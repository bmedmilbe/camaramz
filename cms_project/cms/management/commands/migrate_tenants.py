import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import transaction
from django.conf import settings
from django.utils.timezone import now

# Target consolidated models (cms app)
from cms import models as cms_models

# Source legacy models
from cmz import models as mz_models
from cecab import models as cb_models

class Command(BaseCommand):
    help = 'Migrate all data from legacy tenant apps to the consolidated CMS model'

    def add_arguments(self, parser):
        parser.add_argument('tenant_id', type=int, help='The ID of the target Tenant')
        parser.add_argument('source_app', type=str, help='Source app: "mz" (camaramz) or "cb" (cecab)')

    def copy_s3_file(self, source_file, target_field):
        """
        Streams a file from S3 to the new model without saving locally.
        Django's storage backend handles the transfer.
        """
        if not source_file:
            return
        try:
            filename = os.path.basename(source_file.name)
            target_field.save(filename, ContentFile(source_file.read()), save=False)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"File migration failed for {source_file}: {e}"))

    def handle(self, *args, **options):
        tenant_id = options['tenant_id']
        source = options['source_app']

        self.stdout.write(f"--- Starting Migration: {source} -> Tenant {tenant_id} ---")

        try:
            with transaction.atomic():
                if source == 'mz':
                    self.migrate_camaramz(tenant_id)
                elif source == 'cb':
                    self.migrate_cecab(tenant_id)
                else:
                    self.stdout.write(self.style.ERROR("Invalid source. Use 'mz' or 'cb'."))
                    return

            self.stdout.write(self.style.SUCCESS(f"Migration for {source} completed successfully!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Migration failed: {e}"))

    def migrate_camaramz(self, t_id):
        """Migrates data from CamaraMZ (mz)"""
        
        # 1. Secretary & Sections
        section_map = {}
        for old_sec in mz_models.Section.objects.all():
            new_sec, _ = cms_models.Section.objects.get_or_create(title=old_sec.title, tenant_id=t_id)
            section_map[old_sec.id] = new_sec

        for old_sct in mz_models.Secretary.objects.all():
            new_sct, _ = cms_models.Secretary.objects.get_or_create(user=old_sct.user, tenant_id=t_id)
            for old_rel in mz_models.SecreatarySection.objects.filter(secretary=old_sct):
                cms_models.SecreatarySection.objects.get_or_create(
                    secretary=new_sct,
                    section=section_map.get(old_rel.section_id),
                    tenant_id=t_id
                )

        # 2. Tours & Images
        for old_tour in mz_models.Tour.objects.all():
            new_tour = cms_models.Tour.objects.create(
                title=old_tour.title, slug=old_tour.slug, description=old_tour.description,
                location=old_tour.location, date=old_tour.date, active=old_tour.active,
                tenant_id=t_id
            )
            for img in mz_models.ImagesTour.objects.filter(tour=old_tour):
                new_img = cms_models.ImagesTour(tour=new_tour, tenant_id=t_id)
                self.copy_s3_file(img.image, new_img.image)
                new_img.save()

        # 3. Roles and Team (Including Assembly)
        role_map = {}
        for old_role in mz_models.Role.objects.all():
            new_role, _ = cms_models.Role.objects.get_or_create(title=old_role.title, tenant_id=t_id)
            role_map[old_role.id] = new_role

        for old_team in mz_models.Team.objects.all():
            new_member = cms_models.Team(
                name=old_team.name, role=role_map.get(old_team.role_id),
                from_assembly=False, tenant_id=t_id
            )
            self.copy_s3_file(old_team.image, new_member.image)
            new_member.save()

        for old_ass in mz_models.Assembly.objects.all():
            role_obj, _ = cms_models.Role.objects.get_or_create(title=old_ass.role, tenant_id=t_id)
            new_member = cms_models.Team(
                name=old_ass.name, role=role_obj,
                from_assembly=True, tenant_id=t_id
            )
            self.copy_s3_file(old_ass.image, new_member.image)
            new_member.save()

        # 4. Posts & ExtraDocs
        for old_post in mz_models.Post.objects.all():
            new_post = cms_models.Post(
                title=old_post.title, slug=old_post.slug, user=old_post.user,
                active=old_post.active, date=old_post.date, featured=old_post.featured,
                is_a_service=old_post.is_cmz_service, tenant_id=t_id
            )
            self.copy_s3_file(old_post.picture, new_post.picture)
            self.copy_s3_file(old_post.text_file, new_post.text_file)
            new_post.save()
        
         # 5. Front Post
        for old_front_post in mz_models.Front.objects.all():
            new_post = cms_models.Post(
                title=old_front_post.title, slug=old_front_post.slug, is_to_front=True,
                picture=old_front_post.picture, tenant_id=t_id
            )
            self.copy_s3_file(old_front_post.picture, new_post.picture)
            new_post.save()

    def migrate_cecab(self, t_id):
        """Migrates data from CECAB (cb)"""

        # 1. Partner
        for old_p in cb_models.Pathner.objects.all():
            new_p = cms_models.Partner(title=old_p.title, tenant_id=t_id)
            self.copy_s3_file(old_p.picture, new_p.picture)
            new_p.save()

        # 2. Roles and Team
        role_map = {}
        for old_r in cb_models.Role.objects.all():
            new_r, _ = cms_models.Role.objects.get_or_create(title=old_r.title, tenant_id=t_id)
            role_map[old_r.id] = new_r

        for old_t in cb_models.Team.objects.all():
            new_t = cms_models.Team(
                name=old_t.name, role=role_map.get(old_t.role_id), tenant_id=t_id
            )
            self.copy_s3_file(old_t.picture, new_t.image)
            new_t.save()

        # 3. Districts and Associations
        dist_map = {}
        for d in cb_models.District.objects.all():
            new_d, _ = cms_models.District.objects.get_or_create(name=d.name)
            dist_map[d.id] = new_d

        for old_as in cb_models.Association.objects.all():
            new_as = cms_models.Association(
                name=old_as.name, registered=old_as.registered, address=old_as.address,
                number_of_associated=old_as.number_of_associated,
                district=dist_map.get(old_as.district_id), tenant_id=t_id
            )
            self.copy_s3_file(old_as.picture, new_as.picture)
            new_as.save()

            for img in cb_models.AssociationImages.objects.filter(associaton=old_as):
                new_img = cms_models.AssociationImages(associaton=new_as, tenant_id=t_id)
                self.copy_s3_file(img.image, new_img.image)
                new_img.save()

        # 4. Videos (Bands & Spots)
        for b in cb_models.Band.objects.all():
            v = cms_models.Video(title=b.title, link=b.link, is_band=True, tenant_id=t_id, created_at=now())
            self.copy_s3_file(b.picture, v.picture)
            v.save()

        for s in cb_models.Spot.objects.all():
            v = cms_models.Video(title=s.title, link=s.link, is_spot=True, tenant_id=t_id, created_at=s.created_at)
            self.copy_s3_file(s.picture, v.picture)
            v.save()

        # 5. Year Goals
        for old_g in cb_models.YearGols.objects.all():
            cms_models.YearGoals.objects.create(
                year=old_g.year, associations=old_g.associations,
                agricultors=old_g.agricultors, products=old_g.products,
                tenant_id=t_id
            )

        # 6. Posts & Content
        for old_p in cb_models.Post.objects.all():
            new_p = cms_models.Post(
                title=old_p.title, slug=old_p.slug, active=old_p.active,
                date=old_p.date, tenant_id=t_id
            )
            self.copy_s3_file(old_p.picture, new_p.picture)
            self.copy_s3_file(old_p.text_file, new_p.text_file)
            new_p.save()

            for p_img in cb_models.PostImages.objects.filter(post=old_p):
                new_img = cms_models.PostImage(post=new_p, tenant_id=t_id)
                self.copy_s3_file(p_img.picture, new_img.picture)
                new_img.save()

        # 7. Messages
        for m in cb_models.Messages.objects.all():
            cms_models.Message.objects.create(
                name=m.name, email=m.email, subject=m.subject,
                text=m.text, sent=m.sent, date=m.date, tenant_id=t_id
            )