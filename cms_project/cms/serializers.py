from pprint import pprint

from rest_framework import serializers
from django.conf import settings
from django.core.mail import BadHeaderError, get_connection, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import (
    Association, AssociationImages, Law, Party, President, Video, Budget, District, ExtraDoc,
    ExtraImages, ImagesTour, Information, Message, Partner, Post,
    PostDocument, PostFile, PostImage, PostVideo, Role, SecreatarySection,
    Secretary, Section, Team, Tour, Vote, YearGoals
)
import json
import requests
from io import BytesIO
import timeago
from datetime import datetime, timezone


# Serializers for District (no tenant)
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']


# Association Serializers
class AssociationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssociationImages
        fields = ['id', 'image']


class AssociationSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Association
        fields = ['id', 'name', 'registered', 'address', 'number_of_associated', 'picture']


class AssociationSerializer(serializers.ModelSerializer):
    district = DistrictSerializer(read_only=True)
    cms_images = AssociationImageSerializer(many=True, read_only=True)

    class Meta:
        model = Association
        fields = ['id', 'name', 'registered', 'address', 'number_of_associated',
                  'picture', 'district', 'cms_images']

    def validate_district(self, value):
        if value is None:
            raise serializers.ValidationError("District is required")
        return value


class AssociationCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Association
        fields = ['name', 'registered', 'address', 'number_of_associated', 'picture', 'district']


# Video Serializers
class VideoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'link', 'picture']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'link', 'picture', 'is_band', 'is_spot', 'created_at']


class VideoCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'link', 'picture', 'is_band', 'is_spot', 'created_at']


# Budget Serializers
class BudgetSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'title', 'type', 'year']


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'title', 'slug', 'text_file', 'date', 'year', 'type']


class BudgetCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['title', 'slug', 'text_file', 'year', 'type']


# ExtraDoc and ExtraImages Serializers
class ExtraImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraImages
        fields = ['id', 'picture']


class ExtraDocSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraDoc
        fields = ['id', 'title', 'picture', 'active', 'date']


class ExtraDocSerializer(serializers.ModelSerializer):
    cms_extra_images = ExtraImageSerializer(many=True, read_only=True)

    class Meta:
        model = ExtraDoc
        fields = ['id', 'title', 'slug', 'picture', 'text_file', 'active', 'date', 'cms_extra_images']


class ExtraDocCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraDoc
        fields = ['title', 'slug', 'picture', 'text_file', 'active']


# ImagesTour Serializer
class ImagesTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagesTour
        fields = ['id', 'image']


# Information Serializer
class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = ['id', 'question', 'information', 'service']


class InformationCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = ['question', 'information', 'service']


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'name', 'email', 'subject', 'text', 'sent', 'date']


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'text']

    def create(self, validated_data):
        try:
            email = validated_data['email']
            tenant = self.context.get('request').tenant if self.context.get('request') else None

            # Prefer tenant email settings; fall back to CECAB config
            sender_email = None
            sender_password = None
            logo_url = None

            if tenant:
                sender_email = getattr(tenant, 'contact_email', None)
                sender_password = getattr(tenant, 'email_password', None)
                logo_url = getattr(tenant, 'logo', None)

            if not sender_email:
                sender_email = settings.EMAILS.get('CECAB', {}).get('EMAIL')
            if not sender_password:
                sender_password = settings.EMAILS.get('CECAB', {}).get('PASSWORD')
            if not logo_url:
                logo_url = settings.EMAILS.get('CECAB', {}).get('LOGO')

            convert_to_html_content = render_to_string(
                template_name='emails/message.html',
                context={
                    'message': validated_data['text'],
                    'section': validated_data['subject'],
                    'name': validated_data['name'],
                    'email': validated_data['email'],
                    'logo': logo_url,
                }
            )
            plain_message = strip_tags(convert_to_html_content)

            connection = get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=sender_email,
                password=sender_password,
                use_tls=settings.EMAIL_USE_TLS,
            )

            recipients = {sender_email, email}  # send to tenant + sender (deduplicated)

            send_mail(
                subject=validated_data['subject'],
                message=plain_message,
                from_email=sender_email,
                recipient_list=list(recipients),
                html_message=convert_to_html_content,
                fail_silently=True,
                connection=connection,
            )

            validated_data['sent'] = True
        except BadHeaderError:
            pass

        return super().create(validated_data)


# Partner Serializer
class PartnerSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'title', 'picture']


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'title', 'picture']


# Role Serializer
class RoleSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'title']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'title']


# Post related Serializers
class PostDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostDocument
        fields = ['id', 'document']


class PostFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFile
        fields = ['id', 'file']


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'picture']


class PostVideoSerializer(serializers.ModelSerializer):
    video = VideoSimpleSerializer(read_only=True)

    class Meta:
        model = PostVideo
        fields = ['id', 'video']


class PostSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'picture', 'active', 'featured', 'date']


class PostSerializer(serializers.ModelSerializer):
    beginning = serializers.SerializerMethodField(method_name="get_beginning")
    posted_at = serializers.SerializerMethodField(method_name="get_posted_at")
    text = serializers.CharField(read_only=True)
    post_images = PostImageSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'picture', 'user', 'post_images',
                  'beginning', 'text', 'posted_at', 'date']

    def get_posted_at(self, post: Post):
        """Return time ago format for post date."""
        now = datetime.now(timezone.utc)
        return timeago.format(post.date, now)

    def get_beginning(self, post: Post):
        """Return first 100 chars from description (auto-generated by signal)."""
        if post.description:
            return post.description
        return ""


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'picture', 'text_file', 'active', 'featured',
                  'is_a_service', 'is_social_service', 'is_to_front', 'description']


# Section Serializers
class SectionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'title']


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'title']


# Secretary Serializers
class SecretarySimpleSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Secretary
        fields = ['id', 'user']


class SecretarySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Secretary
        fields = ['id', 'user']


# SecreatarySection Serializer
class SecreatarySectionSerializer(serializers.ModelSerializer):
    section = SectionSimpleSerializer(read_only=True)
    secretary = SecretarySimpleSerializer(read_only=True)

    class Meta:
        model = SecreatarySection
        fields = ['id', 'section', 'secretary']


class SecreatarySectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecreatarySection
        fields = ['section', 'secretary']


# Team Serializers
class TeamSimpleSerializer(serializers.ModelSerializer):
    role = RoleSimpleSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'image', 'role']


class TeamSerializer(serializers.ModelSerializer):
    role = RoleSimpleSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'image', 'role', 'from_assembly']


class TeamCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'image', 'role', 'from_assembly']


# Tour Serializer
class TourSerializer(serializers.ModelSerializer):
    cms_images = ImagesTourSerializer(many=True, read_only=True)

    class Meta:
        model = Tour
        fields = ['id', 'title', 'slug', 'description', 'location', 'date', 'active', 'cms_images']


# YearGoals Serializer
class YearGoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearGoals
        fields = ['id', 'year', 'associations', 'agricultors', 'products']


class PresidentSerializer(serializers.ModelSerializer):

    class Meta:
        model = President
        fields = ['id', 'name', 'slug']


class PartySerializer(serializers.ModelSerializer):

    class Meta:
        model = Party
        fields = ['id', 'name', 'slug']


class VoteSerializer(serializers.ModelSerializer):
    party = PartySerializer(read_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'votes', 'law', 'party']


class LawSerializer(serializers.ModelSerializer):
    an_president = PresidentSerializer(read_only=True)
    stp_president = PresidentSerializer(read_only=True)
    cms_laws_votes_law = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Law
        fields = ['id', 'title', 'slug', 'file', 'published_date', 'cms_laws_votes_law',
                  'aprovation_date', 'an_president', 'stp_president']
