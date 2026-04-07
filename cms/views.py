from rest_framework import viewsets, mixins
from rest_framework.permissions import BasePermission
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    Association, AssociationImages, Video, Budget, District, ExtraDoc, 
    ExtraImages, ImagesTour, Information, Message, Partner, Post, 
    PostDocument, PostFile, PostImage, PostVideo, Role, SecreatarySection, 
    Secretary, Section, Team, Tour, YearGoals
)
from .serializers import (
    AssociationSerializer, AssociationImageSerializer,
    VideoSerializer,
    BudgetSerializer,
    DistrictSerializer,
    ExtraDocSerializer, ExtraImageSerializer,
    ImagesTourSerializer,
    InformationSerializer,
    MessageSerializer, MessageCreateSerializer,
    PartnerSerializer,
    PostSerializer,
    PostDocumentSerializer, PostFileSerializer, PostImageSerializer, PostVideoSerializer,
    RoleSerializer,
    SecreatarySectionSerializer,
    SecretarySerializer,
    SectionSerializer,
    TeamSerializer,
    TourSerializer,
    YearGoalsSerializer
)


class IsTenantUser(BasePermission):
    """
    Permission class to filter by tenant.
    Expects 'request.tenant' to be set by middleware.
    """
    def has_permission(self, request, view):
        return hasattr(request, 'tenant')

    def has_object_permission(self, request, view, obj):
        return obj.tenant == request.tenant


class Pagination300(PageNumberPagination):
    page_size = 300
    page_size_query_param = 'page_size'
    max_page_size = 1000


class Pagination100(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


# District ViewSet (read-only, no tenant)
class DistrictViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = District.objects.all().order_by('name')
    serializer_class = DistrictSerializer
    pagination_class = Pagination300


# Association ViewSet
class AssociationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'address']
    ordering_fields = ['name', 'registered']
    ordering = ['name']
    serializer_class = AssociationSerializer

    def get_queryset(self):
        return Association.objects.optimized().filter(tenant=self.request.tenant).order_by('name')


# Association Images ViewSet
class AssociationImageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    pagination_class = Pagination300
    serializer_class = AssociationImageSerializer

    def get_queryset(self):
        return AssociationImages.objects.filter(tenant=self.request.tenant).select_related('associaton')


# Video ViewSet
class VideoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title']
    ordering_fields = ['title', 'created_at']
    ordering = ['-created_at']
    filterset_fields = ['is_band', 'is_spot']
    serializer_class = VideoSerializer

    def get_queryset(self):
        return Video.objects.filter(tenant=self.request.tenant).order_by('-created_at')


# Budget ViewSet
class BudgetViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    pagination_class = Pagination100
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title']
    ordering_fields = ['title', 'date', 'year', 'type']
    ordering = ['-date']
    filterset_fields = ['type', 'year']
    serializer_class = BudgetSerializer

    def get_queryset(self):
        return Budget.objects.filter(tenant=self.request.tenant).order_by('-date')


# ExtraDoc ViewSet
class ExtraDocViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    lookup_field = 'slug'
    pagination_class = Pagination100
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title']
    ordering_fields = ['title', 'date', 'active']
    ordering = ['-date']
    filterset_fields = ['active']
    serializer_class = ExtraDocSerializer

    def get_queryset(self):
        return ExtraDoc.objects.filter(tenant=self.request.tenant).prefetch_related('cms_extra_images').order_by('-date')


# ExtraImages ViewSet
class ExtraImageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    pagination_class = Pagination300
    serializer_class = ExtraImageSerializer

    def get_queryset(self):
        return ExtraImages.objects.filter(tenant=self.request.tenant)


# ImagesTour ViewSet
class ImagesTourViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    pagination_class = Pagination300
    serializer_class = ImagesTourSerializer

    def get_queryset(self):
        return ImagesTour.objects.filter(tenant=self.request.tenant)


# Information ViewSet
class InformationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    pagination_class = Pagination100
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['question']
    ordering_fields = ['question']
    serializer_class = InformationSerializer

    def get_queryset(self):
        return Information.objects.filter(tenant=self.request.tenant).select_related('service')


# Message ViewSet
class MessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    serializer_class = MessageCreateSerializer

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)


# Partner ViewSet
class PartnerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    pagination_class = Pagination100
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title']
    ordering = ['title']
    serializer_class = PartnerSerializer

    def get_queryset(self):
        return Partner.objects.filter(tenant=self.request.tenant).order_by('title')


# Role ViewSet
class RoleViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    pagination_class = Pagination100
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title']
    ordering = ['title']
    serializer_class = RoleSerializer

    def get_queryset(self):
        return Role.objects.filter(tenant=self.request.tenant).order_by('title')


# Post ViewSet
class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    lookup_field = 'slug'
    
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'date', 'featured']
    ordering = ['-date']
    filterset_fields = ['active', 'featured', 'is_a_service', 'is_social_service', 'is_to_front']
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.optimized().filter(tenant=self.request.tenant).order_by('-date')


# PostDocument ViewSet
class PostDocumentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    pagination_class = Pagination300
    serializer_class = PostDocumentSerializer

    def get_queryset(self):
        return PostDocument.objects.filter(tenant=self.request.tenant)


# PostFile ViewSet
class PostFileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    pagination_class = Pagination300
    serializer_class = PostFileSerializer

    def get_queryset(self):
        return PostFile.objects.filter(tenant=self.request.tenant)


# PostImage ViewSet
class PostImageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    pagination_class = Pagination300
    serializer_class = PostImageSerializer

    def get_queryset(self):
        return PostImage.objects.filter(tenant=self.request.tenant)


# PostVideo ViewSet
class PostVideoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    pagination_class = Pagination300
    serializer_class = PostVideoSerializer

    def get_queryset(self):
        return PostVideo.objects.filter(tenant=self.request.tenant).select_related('video')


# Section ViewSet
class SectionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    pagination_class = Pagination100
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title']
    ordering = ['title']
    serializer_class = SectionSerializer

    def get_queryset(self):
        return Section.objects.filter(tenant=self.request.tenant).order_by('title')


# Secretary ViewSet
class SecretaryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    pagination_class = Pagination100
    serializer_class = SecretarySerializer

    def get_queryset(self):
        return Secretary.objects.filter(tenant=self.request.tenant).select_related('user')


# SecreatarySection ViewSet
class SecreatarySectionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    pagination_class = Pagination100
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['section', 'secretary']
    serializer_class = SecreatarySectionSerializer

    def get_queryset(self):
        return SecreatarySection.objects.filter(tenant=self.request.tenant).select_related(
            'section', 'secretary', 'secretary__user'
        )


# Team ViewSet
class TeamViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    pagination_class = Pagination100
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']
    ordering_fields = ['name', 'role']
    ordering = ['name']
    filterset_fields = ['role', 'from_assembly']
    serializer_class = TeamSerializer

    def get_queryset(self):
        return Team.objects.filter(tenant=self.request.tenant).select_related('role').order_by('name')


# Tour ViewSet
class TourViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    lookup_field = 'slug'
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'date']
    ordering = ['-date']
    filterset_fields = ['active']
    serializer_class = TourSerializer

    def get_queryset(self):
        return Tour.objects.filter(tenant=self.request.tenant).prefetch_related('cms_images').order_by('-date')


# YearGoals ViewSet
class YearGoalsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsTenantUser]
    pagination_class = Pagination100
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['year']
    ordering = ['-year']
    filterset_fields = ['year']
    serializer_class = YearGoalsSerializer

    def get_queryset(self):
        return YearGoals.objects.filter(tenant=self.request.tenant).order_by('-year')
