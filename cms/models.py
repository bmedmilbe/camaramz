from django.db import models
from django.conf import settings
from django.db.models import Prefetch


class CustomerQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related("user__tenant")


class Customer(models.Model):
    objects = CustomerQuerySet.as_manager()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cms_customer")

    level = models.IntegerField(default=1, null=True)
    backstaff = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"


class AsssociationQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related('district', 'tenant').prefetch_related('cms_images')


class Association(models.Model):
    objects = AsssociationQuerySet.as_manager()
    name = models.CharField(max_length=255)
    registered = models.DateField()
    address = models.CharField(max_length=255)
    number_of_associated = models.IntegerField()
    picture = models.FileField(upload_to='mt_api/cms/association_images')
    district = models.ForeignKey(
        "District", on_delete=models.CASCADE, related_name="cms_associations")

    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_associations")

    def __str__(self) -> str:
        return f'{self.name}'


class AssociationImages(models.Model):
    associaton = models.ForeignKey(
        Association, on_delete=models.CASCADE, related_name="cms_images")
    image = models.FileField(upload_to='mt_api/cms/association_images/')
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_association_images")


class Video(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    picture = models.FileField(upload_to='mt_api/cms/video_images/', null=True, blank=True)
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_videos")
    is_band = models.BooleanField(default=False)
    is_spot = models.BooleanField(default=False)
    created_at = models.DateField()


class Budget(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True)
    text_file = models.FileField(upload_to='mt_api/cms/docs/documents/')
    date = models.DateTimeField(auto_now_add=True)
    year = models.IntegerField(null=True, blank=True)

    TYPE_BUDGET = "B"
    TYPE_REPORT = "R"
    TYPE_LAW = "L"
    STATUS_CHOICES = [
        (TYPE_BUDGET, "Budget"),
        (TYPE_REPORT, "Report"),
        (TYPE_LAW, "Law"),
    ]
    type = models.CharField(max_length=1, choices=STATUS_CHOICES)
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_budgets")

    def __str__(self) -> str:
        return f'{self.title}'


class District(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.name}'


class ExtraDoc(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True)
    picture = models.FileField(upload_to='mt_api/cms/posts/images/', null=True)
    text_file = models.FileField(upload_to='mt_api/cms/posts/documents/')
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_extra_docs")

    def __str__(self) -> str:
        return f'{self.title}'


class ExtraImages(models.Model):
    picture = models.FileField(upload_to='mt_api/cms/extras/images/')
    extra_doc = models.ForeignKey(
        ExtraDoc, on_delete=models.CASCADE, related_name="cms_extra_images")
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_extra_images")


class ImagesTour(models.Model):
    tour = models.ForeignKey(
        "Tour", on_delete=models.CASCADE, related_name="cms_images")
    image = models.FileField(upload_to='mt_api/cms/tour/images/')
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_images_tours")


class Information(models.Model):
    service = models.ForeignKey("Post", on_delete=models.PROTECT, related_name="informations")
    information = models.TextField()
    question = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.question}'
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_informations")


class Message(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    text = models.TextField()
    sent = models.BooleanField(default=False, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_messages")

    def __str__(self) -> str:
        return f'{self.name}'


class Partner(models.Model):
    title = models.CharField(max_length=255)
    picture = models.FileField(upload_to='mt_api/cms/partner_images/')
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_partner")

    def __str__(self) -> str:
        return f'{self.title}'


class PostQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related('user__tenant', 'tenant')\
            .prefetch_related('post_images', 'post_videos', 'cms_files', 'documents', 'informations')


class Post(models.Model):
    objects = PostQuerySet.as_manager()
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True)
    picture = models.FileField(upload_to='mt_api/cms/posts/images/')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="cms_posts",
        blank=True)
    text_file = models.FileField(upload_to='mt_api/cms/posts/documents/', null=True, max_length=500, blank=True)
    processed_text_file = models.FileField(
        upload_to='mt_api/cms/posts/processed/',
        null=True,
        max_length=500,
        blank=True,
        help_text="Auto-generated JSON file with processed HTML content")
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    is_a_service = models.BooleanField(default=False)
    is_social_service = models.BooleanField(default=False)
    is_to_front = models.BooleanField(default=False)
    description = models.TextField(default="Através desse seviço, estarás habilitado para ...", null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_posts")

    def __str__(self) -> str:
        return f'{self.title}'


class PostDocument(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='mt_api/cms/post/documents/')
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_post_documents")


class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="cms_files")
    file = models.FileField(upload_to='mt_api/cms/posts/file/')
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_post_files")


class PostImage(models.Model):
    picture = models.FileField(upload_to='mt_api/cms/posts/images/')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_images")
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_post_images")


class PostVideo(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="post_videos", null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_videos", null=True)
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_post_videos")


class Role(models.Model):
    title = models.CharField(max_length=255)
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_role")

    def __str__(self) -> str:
        return f'{self.title}'


class SecreatarySection(models.Model):
    section = models.ForeignKey("Section", on_delete=models.CASCADE, related_name="secreatary_sections")
    secretary = models.ForeignKey("Secretary", on_delete=models.CASCADE, related_name="secreatary_sections")
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_secretary_sections")


class Secretary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cms_secretaries")
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_secretaries")

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'


class Section(models.Model):
    title = models.CharField(max_length=255)
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_sections")

    def __str__(self) -> str:
        return f'{self.title}'


class Team(models.Model):
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to='mt_api/cms/team/images/', null=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='teams')
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_teams")
    from_assembly = models.BooleanField(default=False)

    class Meta():
        unique_together = ['name', 'role', 'tenant']

    def __str__(self) -> str:
        return f'{self.name} - {self.role}'


class TourQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related('tenant').prefetch_related('cms_images')


class Tour(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    location = models.URLField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(default=False)
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_tours")

    def __str__(self) -> str:
        return self.title


class YearGoals(models.Model):
    year = models.IntegerField()
    associations = models.IntegerField()
    agricultors = models.IntegerField()
    products = models.DecimalField(max_digits=10, decimal_places=2)
    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_year_goals")


class President(models.Model):
    name = models.TextField(unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Party(models.Model):
    name = models.TextField(unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class LawQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related('an_president', 'stp_president', 'tenant')


class Law(models.Model):
    objects = LawQuerySet.as_manager()
    title = models.TextField(unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    file = models.FileField(upload_to='mt_api/cms/laws/file/')

    published_date = models.DateField()
    aprovation_date = models.DateField()
    an_president = models.ForeignKey(President, on_delete=models.CASCADE, related_name="cms_laws_an_president")
    stp_president = models.ForeignKey(President, on_delete=models.CASCADE, related_name="cms_laws_stp_president")

    tenant = models.ForeignKey(
        settings.TENANT_MODEL, on_delete=models.CASCADE, related_name="cms_laws")

    def __str__(self) -> str:
        return self.title


class VoteQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related('party', 'law')


class Vote(models.Model):
    objects = VoteQuerySet.as_manager()
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name="cms_laws_votes_party")
    law = models.ForeignKey(Law, on_delete=models.CASCADE, related_name="cms_laws_votes_law")
    votes = models.IntegerField()

    class Meta:
        unique_together = ['party', 'law']
