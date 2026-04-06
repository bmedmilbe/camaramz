from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from certificates.permission import IsStaff
from certificates.serializers import (
    BiuldingTypeSerializer, CemiterioSerializer, CertificateCommentSerializer, 
    CertificateDateSerializer, CertificateModelAutoConstrucaoCreateSerializer, 
    CertificateModelAutoConstrucaoSerializer, CertificateModelAutoModCovalCreateSerializer, 
    CertificateModelAutoModCovalSerializer, CertificateModelCertCompraCovalCreateSerializer, 
    CertificateModelCertCompraCovalSerializer, CertificateModelEnterroCreateSerializer, 
    CertificateModelEnterroSerializer, CertificateModelFifthCreateSerializer, 
    CertificateModelFifthSerializer, CertificateModelLicBarracaCreateSerializer, 
    CertificateModelLicBarracaSerializer, CertificateModelLicencaBuffetCreateSerializer, 
    CertificateModelLicencaBuffetSerializer, CertificateModelOneCreateSerializer, 
    CertificateModelOneSerializer, CertificateModelSeventhCreateSerializer, 
    CertificateModelSeventhSerializer, CertificateModelThreeCreateSerializer, 
    CertificateModelThreeSerializer, CertificateModelTwoCreateSerializer, 
    CertificateModelTwoSerializer, CertificateSerializer, 
    CertificateSimpleParentSerializer, CertificateSimplePersonReadOnlySerializer, 
    CertificateSimplePersonSerializer, CertificateSinglePersonSerializer, 
    CertificateTitleSerializer, CertificateUpdateSerializer, ChangeSerializer, 
    CountryCreateSerializer, CountrySerializer, CountyCreateSerializer, 
    CountySerializer, CovalSerializer, CovalSetUpSerializer, CustomerSerializer, 
    HouseCreateSerializer, HouseSerializer, IDTypeSerializer, IfenSerializer, 
    IfenUpdateSerializer, InstituitionCreateSerializer, InstituitionSerializer, 
    MetadataSerializer, ParentSerializer, PersonBirthAddressCreateSerializer, 
    PersonBirthAddressSerializer, PersonCreateOrUpdateSerializer, PersonSerializer, 
    StreetCreateSerializer, StreetSerializer, TownCreateSerializer, 
    TownSerializer, UniversityCreateSerializer, UniversitySerializer
)

from .models import (
    BiuldingType, Cemiterio, CertificateDate, CertificateSimpleParent, 
    CertificateSimplePerson, CertificateSinglePerson, CertificateTitle, 
    Change, Country, County, Coval, Customer, House, IDType, Ifen, 
    Instituition, Certificate, Parent, Person, PersonBirthAddress, 
    Street, Town, University
)
from .helpers import get_customer


class Pagination300(PageNumberPagination):
    page_size = 500
    page_size_query_param = 'page_size'
    max_page_size = 5000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CountrysViewSet(ModelViewSet):
    queryset = Country.objects.all().order_by("name")
    pagination_class = Pagination300
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return CountryCreateSerializer
        return CountrySerializer


class CovalsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Coval.objects.select_related("cemiterio").all().order_by("number")
    serializer_class = CovalSerializer
    pagination_class = Pagination300


class CemiteriosViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Cemiterio.objects.select_related("county").all().order_by("name")
    serializer_class = CemiterioSerializer
    pagination_class = Pagination300


class ChangesViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Change.objects.all()
    serializer_class = ChangeSerializer
    pagination_class = Pagination300


class UniversitysViewSet(ModelViewSet):
    queryset = University.objects.all().order_by("name")
    pagination_class = Pagination300
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return University.objects.all().order_by("name")

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return UniversityCreateSerializer
        return UniversitySerializer


class IdTypeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = IDType.objects.all().order_by("name")
    serializer_class = IDTypeSerializer
    pagination_class = Pagination300


class BiuldingTypeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = BiuldingType.objects.all().order_by("name")
    serializer_class = BiuldingTypeSerializer
    pagination_class = Pagination300


class StreetsViewSet(ModelViewSet):
    pagination_class = Pagination300
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return StreetCreateSerializer
        return StreetSerializer

    def get_queryset(self):
        return Street.objects.select_related("town", "county").all().order_by("name")


class IfenViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return IfenUpdateSerializer
        return IfenSerializer

    def get_queryset(self):
        return Ifen.objects.all()


class MetadataViewSet(viewsets.ViewSet):
    """Unified metadata endpoint to prevent waterfall lag."""
    def list(self, request):
        data = {
            "countries": Country.objects.all().order_by('name'),
            "universities": University.objects.all().order_by('name'),
            "ifens": Ifen.objects.all().order_by('name'),
            "buildings": BiuldingType.objects.all().order_by('name'),
            "cemiterios": Cemiterio.objects.select_related('county').all().order_by('name'),
            "streets": Street.objects.select_related('town', 'county').all().order_by('name'),
            "changes": Change.objects.all().order_by('name'),
            "towns": Town.objects.select_related('county').all().order_by('name'),
            "countys": County.objects.select_related('country').all().order_by('name'),
            "certificateTitles": CertificateTitle.objects.select_related('certificate_type').all().order_by('name'),
            "covals": Coval.objects.select_related("cemiterio").all().order_by('number'),
            "idtypes": IDType.objects.all().order_by('name'),
            "intituitions": Instituition.objects.all().order_by('name'),
        }
        serializer = MetadataSerializer(data)
        return Response(serializer.data)


class InstituitionsViewSet(ModelViewSet):
    pagination_class = Pagination300
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return InstituitionCreateSerializer
        return InstituitionSerializer

    def get_queryset(self):
        return Instituition.objects.all().order_by("name")


class CustomerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Customer.objects.select_related("user").filter(user_id=self.request.user)

    def get_serializer_class(self):
        return CustomerSerializer

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = get_customer(request.user)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


class CovalSetUpViewSet(ModelViewSet):
    queryset = Coval.objects.select_related("cemiterio").all().order_by("square", "-number")
    permission_classes = [IsStaff]
    pagination_class = Pagination300

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CovalSerializer
        return CovalSetUpSerializer


class CertificateViewSet(
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin, 
    mixins.DestroyModelMixin, 
    GenericViewSet
    ):
    queryset = Certificate.objects.select_related(
        "type__certificate_type", 
        'main_person__id_type',
        'main_person__id_issue_local',
        'main_person__id_issue_country',
        'main_person__nationality',
        'main_person__birth_address',
        'main_person__address',
        'main_person__birth_address__birth_street__town__county__country',
        'main_person__birth_address__birth_town__county__country',
        'main_person__birth_address__birth_county__country',
        'main_person__birth_address__birth_country',
        'main_person__address__street__town__county__country',
        'main_person__address__street__county__country',
        "house__street__county__country", 
        "secondary_person",
        'secondary_person__id_type',
        'secondary_person__id_issue_local',
        'secondary_person__id_issue_country',
        'secondary_person__nationality',
        'secondary_person__birth_address',
        'secondary_person__address',
        'secondary_person__birth_address__birth_street__town__county__country',
        'secondary_person__birth_address__birth_town__county__country',
        'secondary_person__birth_address__birth_county__country',
        'secondary_person__birth_address__birth_country',
        'secondary_person__address__street__town__county__country',
        'secondary_person__address__street__county__country',                                          ).order_by("-id")
    pagination_class = PageNumberPagination
    permission_classes = [IsStaff]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['main_person__name', 'main_person__surname', 'number__startswith', "main_person__id_number", "main_person__birth_date"]
    filterset_fields = {'status': ['exact'], 'type__certificate_type': ['exact', 'gt', 'lte']}
    ordering_fields = ['number', "main_person__name", "main_person__id_number", "main_person__birth_date", "date_issue"]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return CertificateUpdateSerializer
        return CertificateSerializer


class CertificateCommentViewSet(mixins.UpdateModelMixin, GenericViewSet):
    queryset = Certificate.objects.select_related("type", "main_person", "house", "secondary_person").order_by("-id").all()

    def get_serializer_class(self):
        return CertificateCommentSerializer


class CertificateTitleViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = CertificateTitle.objects.select_related("certificate_type").order_by("name").all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'certificate_type': ['exact', 'gt', 'lt']}
    pagination_class = Pagination300

    def get_serializer_class(self):
        return CertificateTitleSerializer


class CertificateModelViewSet(ModelViewSet):
    def get_queryset(self):
        return Certificate.objects.select_related("type", "main_person", "house", "secondary_person").order_by("-id")

    def get_serializer_class(self):
        type_id = int(self.kwargs.get('title_pk'))
        if self.request.method in ["POST", "PUT", "PATCH"]:
            if type_id in [1, 5, 6, 7, 9, 10, 11, 15, 16, 17, 19, 20, 21, 22, 30, 34, 68, 35]:
                return CertificateModelOneCreateSerializer
            elif type_id in [2, 4, 8]:
                return CertificateModelThreeCreateSerializer
            elif type_id in [3, 13]:
                return CertificateModelTwoCreateSerializer
            elif type_id == 12:
                return CertificateModelFifthCreateSerializer
            elif type_id == 18:
                return CertificateModelSeventhCreateSerializer
            elif type_id in [23, 28]:
                return CertificateModelAutoConstrucaoCreateSerializer
            elif type_id in [29, 32]:
                return CertificateModelLicencaBuffetCreateSerializer
            elif type_id == 24:
                return CertificateModelCertCompraCovalCreateSerializer
            elif type_id == 25:
                return CertificateModelAutoModCovalCreateSerializer
            elif type_id == 27:
                return CertificateModelLicBarracaCreateSerializer
            elif type_id == 33:
                return CertificateModelEnterroCreateSerializer

        if type_id == 2:
            return CertificateModelThreeSerializer
        elif type_id in [3, 13]:
            return CertificateModelTwoSerializer
        elif type_id == 12:
            return CertificateModelFifthSerializer
        elif type_id == 18:
            return CertificateModelSeventhSerializer
        elif type_id in [23, 28]:
            return CertificateModelAutoConstrucaoSerializer
        elif type_id in [24, 30]:
            return CertificateModelCertCompraCovalSerializer
        elif type_id == 25:
            return CertificateModelAutoModCovalSerializer
        elif type_id == 27:
            return CertificateModelLicBarracaSerializer
        elif type_id in [29, 31]:
            return CertificateModelLicencaBuffetSerializer
        elif type_id == 32:
            return CertificateModelEnterroSerializer
        
        return CertificateModelOneSerializer

    def get_serializer_context(self):
        return {"type_id": self.kwargs.get('title_pk')}


class CertificatePersonsViewSet(ModelViewSet):
    def get_queryset(self):
        type_id = int(self.kwargs.get('title_pk'))
        if type_id == 12:
            return CertificateSimplePerson.objects.filter(type_id=type_id)
        return CertificateSimplePerson.objects.filter(type_id=-1)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CertificateSimplePersonReadOnlySerializer
        return CertificateSimplePersonSerializer

    def get_serializer_context(self):
        return {"type_id": self.kwargs.get('title_pk')}


class CertificateSimpleParentsViewSet(ModelViewSet):
    def get_queryset(self):
        type_id = int(self.kwargs.get('title_pk'))
        return CertificateSimpleParent.objects.filter(type_id=type_id)

    def get_serializer_class(self):
        return CertificateSimpleParentSerializer

    def get_serializer_context(self):
        return {"type_id": self.kwargs.get('title_pk')}


class ParentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    def get_queryset(self):
        return Parent.objects.all().order_by("id")

    def get_serializer_class(self):
        return ParentSerializer


class CertificateSinglePersonsViewSet(ModelViewSet):
    def get_queryset(self):
        type_id = int(self.kwargs.get('title_pk'))
        if type_id == 12:
            return CertificateSinglePerson.objects.select_related("type").filter(type_id=type_id).all()
        return CertificateSinglePerson.objects.select_related("type").filter(type_id=-1)

    def get_serializer_class(self):
        return CertificateSinglePersonSerializer

    def get_serializer_context(self):
        return {"type_id": self.kwargs.get('title_pk')}


class CertificateDatesViewSet(ModelViewSet):
    def get_queryset(self):
        type_id = int(self.kwargs.get('title_pk'))
        return CertificateDate.objects.select_related("type").filter(type_id=type_id).all()

    def get_serializer_class(self):
        return CertificateDateSerializer

    def get_serializer_context(self):
        return {"type_id": self.kwargs.get('title_pk')}





class PersonBirthAddressViewSet(ModelViewSet):
    queryset = PersonBirthAddress.objects.select_related("birth_county", 
                                                         "birth_town", 
                                                         "birth_country",
                                                         "birth_address").all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PersonBirthAddressCreateSerializer
        return PersonBirthAddressSerializer


class CountysViewSet(ModelViewSet):
    queryset = County.objects.select_related("country").all().order_by("name")
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = Pagination300

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return CountyCreateSerializer
        return CountySerializer


class TownViewSet(ModelViewSet):
    queryset = Town.objects.select_related("county").all().order_by("name")
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = Pagination300

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return TownCreateSerializer
        return TownSerializer


class HouseViewSet(ModelViewSet):
    queryset = House.objects.select_related("street").all().order_by("street__name", "house_number")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return HouseCreateSerializer
        return HouseSerializer


class PersonViewSet(

    mixins.ListModelMixin, mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin, 
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    GenericViewSet
):
    permission_classes = [IsStaff]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'surname', "id_number", "birth_date"]
    ordering_fields = ["name", "id_number", "birth_date", "id_issue_date"]

    def get_queryset(self):
        return Person.objects.select_related(
        'id_type',
        'id_issue_local',
        'id_issue_country',
        'nationality',
        'birth_address',
        'address',

        'birth_address__birth_street__town__county__country',
        'birth_address__birth_town__county__country',
        'birth_address__birth_county__country',
        'birth_address__birth_country',

        'address__street__town__county__country',
        'address__street__county__country',
    ).all()

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT"]:
            return PersonCreateOrUpdateSerializer
        return PersonSerializer

    def get_serializer_context(self):
        return {"id": self.kwargs.get('pk')}