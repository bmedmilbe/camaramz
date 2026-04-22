"""REST API views for the certificates application.

Provides ViewSets for all certificate-related resources including locations,
persons, certificates, and administrative data. Implements dynamic serializer
selection, filtering, searching, and permission-based access control.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from certificates.permission import IsStaff
from certificates.serializers import (
    BiuldingTypeSerializer, CemiterioSerializer, CertificateCommentSerializer,
    CertificateDateSerializer, CertificateModelAutoConstrucaoCreateSerializer,
    CertificateModelAutoModCovalCreateSerializer,
    CertificateModelCertCompraCovalCreateSerializer,
    CertificateModelEnterroCreateSerializer,
    CertificateModelFifthCreateSerializer,
    CertificateModelLicBarracaCreateSerializer,
    CertificateModelLicencaBuffetCreateSerializer,
    CertificateModelOneCreateSerializer,
    CertificateModelSeventhCreateSerializer,
    CertificateModelThreeCreateSerializer,
    CertificateModelTwoCreateSerializer,
    CertificateSerializer,
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
    """Pagination class for large result sets.

    Provides 500 results per page with configurable page size up to 5000 items.
    Used for endpoints expected to return many results.
    """
    page_size = 500
    page_size_query_param = 'page_size'
    max_page_size = 5000


class StandardResultsSetPagination(PageNumberPagination):
    """Pagination class for standard result sets.

    Provides 100 results per page with configurable page size up to 1000 items.
    Used for most endpoints with moderate result sizes.
    """
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CountrysViewSet(ModelViewSet):
    """API endpoint for managing countries.

    Provides full CRUD operations for Country model with support for
    authenticated users to create/update and public read access.
    Dynamically selects serializer based on HTTP method.
    """
    queryset = Country.objects.all().order_by("name")
    pagination_class = Pagination300
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """Select serializer based on request method.

        Returns:
            Serializer: CountryCreateSerializer for POST/PUT/PATCH, CountrySerializer for GET.
        """
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return CountryCreateSerializer
        return CountrySerializer


class CovalsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """API endpoint for retrieving burial plots (read-only).

    Provides list and detail endpoints for Coval (burial plot) models
    with optimized database queries using select_related.
    """
    queryset = Coval.objects.optimized().all().order_by("number")
    serializer_class = CovalSerializer
    pagination_class = Pagination300


class CemiteriosViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """API endpoint for retrieving cemeteries (read-only).

    Provides list and detail endpoints for Cemiterio (cemetery) models
    with optimized database queries.
    """
    queryset = Cemiterio.objects.optimized().all().order_by("name")
    serializer_class = CemiterioSerializer
    pagination_class = Pagination300


class ChangesViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """API endpoint for retrieving price changes and modifications (read-only).

    Provides list and detail endpoints for Change (modification fee) models.
    """
    queryset = Change.objects.all()
    serializer_class = ChangeSerializer
    pagination_class = Pagination300


class UniversitysViewSet(ModelViewSet):
    """API endpoint for managing educational institutions.

    Provides full CRUD operations for University model with support for
    authenticated users to create/update and public read access.
    """
    queryset = University.objects.all().order_by("name")
    pagination_class = Pagination300
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Return universities ordered by name.

        Returns:
            QuerySet: All universities ordered alphabetically.
        """
        return University.objects.all().order_by("name")

    def get_serializer_class(self):
        """Select serializer based on request method.

        Returns:
            Serializer: UniversityCreateSerializer for POST/PUT/PATCH, UniversitySerializer for GET.
        """
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return UniversityCreateSerializer
        return UniversitySerializer


class IdTypeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """API endpoint for retrieving ID types (read-only).

    Provides list and detail endpoints for IDType (identification document type) models.
    """
    queryset = IDType.objects.all().order_by("name")
    serializer_class = IDTypeSerializer
    pagination_class = Pagination300


class BiuldingTypeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """API endpoint for retrieving building types (read-only).

    Provides list and detail endpoints for BiuldingType (structure type) models.
    """
    queryset = BiuldingType.objects.all().order_by("name")
    serializer_class = BiuldingTypeSerializer
    pagination_class = Pagination300


class StreetsViewSet(ModelViewSet):
    """API endpoint for managing streets and roads.

    Provides full CRUD operations for Street model with support for
    authenticated users to create/update and public read access.
    Uses optimized queries with location hierarchy select_related.
    """
    pagination_class = Pagination300
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """Select serializer based on request method.

        Returns:
            Serializer: StreetCreateSerializer for POST/PUT/PATCH, StreetSerializer for GET.
        """
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return StreetCreateSerializer
        return StreetSerializer

    def get_queryset(self):
        """Return optimized queryset of streets.

        Returns:
            QuerySet: Optimized streets with location data pre-fetched, ordered by name.
        """
        return Street.objects.optimized().all().order_by("name")


class IfenViewSet(ModelViewSet):
    """API endpoint for managing IFEN classifications.

    Provides full CRUD operations for Ifen (size/classification) model with
    support for authenticated users to create/update and public read access.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """Select serializer based on request method.

        Returns:
            Serializer: IfenUpdateSerializer for PUT/PATCH, IfenSerializer for others.
        """
        if self.request.method in ["PUT", "PATCH"]:
            return IfenUpdateSerializer
        return IfenSerializer

    def get_queryset(self):
        """Return all Ifen objects.

        Returns:
            QuerySet: All Ifen instances.
        """
        return Ifen.objects.all()


class MetadataViewSet(viewsets.ViewSet):
    """Unified metadata endpoint to prevent API waterfall requests.

    Returns all reference data (countries, locations, certificate types, etc.)
    in a single response to minimize client-side API calls.
    """

    def list(self, request):
        """Retrieve all metadata in a single response.

        Args:
            request: HTTP request object.

        Returns:
            Response: Dictionary containing all reference data with keys for each entity type.
        """
        data = {
            "countries": Country.objects.all().order_by('name'),
            "universities": University.objects.all().order_by('name'),
            "ifens": Ifen.objects.all().order_by('name'),
            "buildings": BiuldingType.objects.all().order_by('name'),
            "cemiterios": Cemiterio.objects.optimized().all().order_by('name'),
            "streets": Street.objects.optimized().all().order_by('name'),
            "changes": Change.objects.all().order_by('name'),
            "towns": Town.objects.optimized().all().order_by('name'),
            "countys": County.objects.optimized().all().order_by('name'),
            "certificateTitles": CertificateTitle.objects.optimized().all().order_by('name'),
            "covals": Coval.objects.optimized().all().order_by('number'),
            "idtypes": IDType.objects.all().order_by('name'),
            "intituitions": Instituition.objects.all().order_by('name'),
        }
        serializer = MetadataSerializer(data)
        return Response(serializer.data)


class InstituitionsViewSet(ModelViewSet):
    """API endpoint for managing institutions.

    Provides full CRUD operations for Instituition (ID-issuing institution) model
    with support for authenticated users to create/update and public read access.
    """
    pagination_class = Pagination300
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """Select serializer based on request method.

        Returns:
            Serializer: InstituitionCreateSerializer for POST/PUT/PATCH, InstituitionSerializer for GET.
        """
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return InstituitionCreateSerializer
        return InstituitionSerializer

    def get_queryset(self):
        """Return institutions ordered by name.

        Returns:
            QuerySet: All institutions ordered alphabetically.
        """
        return Instituition.objects.all().order_by("name")


class CustomerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """API endpoint for retrieving customer records (read-only).

    Provides list and detail endpoints for Customer (staff user) models.
    Includes a custom 'me' action to retrieve the current user's customer record.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Return optimized customer queryset for current user.

        Returns:
            QuerySet: Customer records for the authenticated user.
        """
        return Customer.objects.optimized().filter(user_id=self.request.user)

    def get_serializer_class(self):
        """Return customer serializer.

        Returns:
            Serializer: CustomerSerializer.
        """
        return CustomerSerializer

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Retrieve current user's customer record.

        Args:
            request: HTTP request object with authenticated user.

        Returns:
            Response: Customer data for the authenticated user.
        """
        customer = get_customer(request.user)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


class CovalSetUpViewSet(ModelViewSet):
    """API endpoint for managing burial plot setup and configuration.

    Restricted to staff members. Allows viewing burial plots and updating
    their configuration (via CovalSetUpSerializer on write operations).
    """
    queryset = Coval.objects.optimized().all().order_by("square", "-number")
    permission_classes = [IsStaff]
    pagination_class = Pagination300

    def get_serializer_class(self):
        """Select serializer based on request method.

        Returns:
            Serializer: CovalSerializer for GET, CovalSetUpSerializer for modifications.
        """
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
    """API endpoint for managing issued certificates (staff-only).

    Restricted to staff members. Provides list, retrieve, update, and delete
    operations for Certificate model with support for filtering, searching,
    and ordering across multiple fields.

    Search fields: person name/surname, certificate number, ID number, birth date.
    Filter fields: status, certificate type.
    Ordering fields: number, person name/ID/birth date, issuance date.
    """
    queryset = Certificate.objects.optimized().order_by("-id")
    pagination_class = PageNumberPagination
    permission_classes = [IsStaff]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = [
        'main_person__name',
        'main_person__surname',
        'number__startswith',
        "main_person__id_number",
        "main_person__birth_date"]
    filterset_fields = {'status': ['exact'], 'type__certificate_type': ['exact', 'gt', 'lte']}
    ordering_fields = ['number', "main_person__name", "main_person__id_number", "main_person__birth_date", "date_issue"]

    def get_serializer_class(self):
        """Select serializer based on request method.

        Returns:
            Serializer: CertificateUpdateSerializer for PUT/PATCH/DELETE, CertificateSerializer for GET.
        """
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return CertificateUpdateSerializer
        return CertificateSerializer


class CertificateCommentViewSet(mixins.UpdateModelMixin, GenericViewSet):
    """API endpoint for updating certificate comments/observations.

    Restricted update operations on Certificate records for adding notes and comments.
    """
    queryset = Certificate.objects.optimized().order_by("-id").all()

    def get_serializer_class(self):
        """Return certificate comment serializer.

        Returns:
            Serializer: CertificateCommentSerializer.
        """
        return CertificateCommentSerializer


class CertificateTitleViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """API endpoint for retrieving certificate title/variant definitions (read-only).

    Provides list and detail endpoints with filtering by certificate type.
    """
    queryset = CertificateTitle.objects.optimized().order_by("name").all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'certificate_type': ['exact', 'gt', 'lt']}
    pagination_class = Pagination300

    def get_serializer_class(self):
        """Return certificate title serializer.

        Returns:
            Serializer: CertificateTitleSerializer.
        """
        return CertificateTitleSerializer


class CertificateModelViewSet(
        mixins.UpdateModelMixin,
        mixins.CreateModelMixin,
        GenericViewSet):
    """API endpoint for certificate model creation and updates with dynamic serializer selection.

    Maps certificate type IDs to specific serializer classes for generating certificates
    using different document templates and business logic. Uses an efficient O(1) lookup
    via dictionary mapping.

    Supports certificate types:
    - Model One: Basic certificates (type IDs: default)
    - Model Two: Professional credentials (type IDs: 3, 13)
    - Model Three: Specialized documents (type IDs: 2, 4, 8)
    - Fifth: Specific variant (type ID: 12)
    - Seventh: Specific variant (type ID: 18)
    - Auto-Construção: Building-related (type IDs: 23, 28)
    - Auto-Mod-Coval: Burial-related (type ID: 25)
    - Cert-Compa-Coval: Burial comparison (type ID: 24)
    - Lic-Barraca: Tent license (type ID: 27)
    - Lic-Buffet: Catering license (type IDs: 29, 32)
    - Enterro: Burial-related (type ID: 33)
    """

    def get_queryset(self):
        """Return optimized queryset of certificates.

        Returns:
            QuerySet: Certificates ordered by ID descending, with relations pre-fetched.
        """
        return Certificate.objects.optimized().order_by("-id")

    def get_serializer_class(self):
        """Dynamically select serializer based on certificate title type ID.

        Uses a mapping dictionary for O(1) lookup efficiency. Falls back to
        CertificateModelOneCreateSerializer for unknown type IDs.

        Returns:
            Serializer: Appropriate serializer class for the certificate type.
        """
        # Handle updates first
        if self.request.method in ["PUT", "PATCH"]:
            return CertificateUpdateSerializer

        # Extract and convert the Title ID from nested router context
        try:
            type_id = int(self.kwargs.get('title_pk', 0))
        except (ValueError, TypeError):
            return CertificateModelOneCreateSerializer

        # Mapping of certificate type IDs to serializer classes
        serializer_map = {
            # Model Three IDs
            2: CertificateModelThreeCreateSerializer,
            4: CertificateModelThreeCreateSerializer,
            8: CertificateModelThreeCreateSerializer,

            # Model Two IDs
            3: CertificateModelTwoCreateSerializer,
            13: CertificateModelTwoCreateSerializer,

            # Individual Assignments
            12: CertificateModelFifthCreateSerializer,
            18: CertificateModelSeventhCreateSerializer,
            24: CertificateModelCertCompraCovalCreateSerializer,
            25: CertificateModelAutoModCovalCreateSerializer,
            27: CertificateModelLicBarracaCreateSerializer,
            33: CertificateModelEnterroCreateSerializer,

            # Auto-Construção IDs
            23: CertificateModelAutoConstrucaoCreateSerializer,
            28: CertificateModelAutoConstrucaoCreateSerializer,

            # Licença Buffet IDs
            29: CertificateModelLicencaBuffetCreateSerializer,
            32: CertificateModelLicencaBuffetCreateSerializer,
        }

        # Return mapped serializer or default (Model One)
        return serializer_map.get(type_id, CertificateModelOneCreateSerializer)

    def get_serializer_context(self):
        """Provide certificate type ID in serializer context.

        Returns:
            dict: Dictionary with 'type_id' key from nested router.
        """
        return {"type_id": self.kwargs.get('title_pk')}


class CertificatePersonsViewSet(ModelViewSet):
    """API endpoint for managing simple person records linked to certificates.

    Used to manage person records with minimal data for specific certificate types.
    Only returns records for type ID 12; other type IDs return empty queryset.
    """

    def get_queryset(self):
        """Return person records for the specified certificate type.

        Returns:
            QuerySet: CertificateSimplePerson records for type_id, empty for non-matching types.
        """
        type_id = int(self.kwargs.get('title_pk'))
        if type_id == 12:
            return CertificateSimplePerson.objects.filter(type_id=type_id)
        return CertificateSimplePerson.objects.filter(type_id=-1)

    def get_serializer_class(self):
        """Select serializer based on request method.

        Returns:
            Serializer: CertificateSimplePersonReadOnlySerializer for GET, CertificateSimplePersonSerializer for modifications.
        """
        if self.request.method == "GET":
            return CertificateSimplePersonReadOnlySerializer
        return CertificateSimplePersonSerializer

    def get_serializer_context(self):
        """Provide certificate type ID in serializer context.

        Returns:
            dict: Dictionary with 'type_id' key from nested router.
        """
        return {"type_id": self.kwargs.get('title_pk')}


class CertificateSimpleParentsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """API endpoint for retrieving parent/family relationship records for certificates (read-only).

    Provides access to parent designation records linked to certificate types.
    """

    def get_queryset(self):
        """Return parent records for the specified certificate type.

        Returns:
            QuerySet: CertificateSimpleParent records for the certificate type_id.
        """
        type_id = int(self.kwargs.get('title_pk'))
        return CertificateSimpleParent.objects.filter(type_id=type_id)

    def get_serializer_class(self):
        """Return parent serializer.

        Returns:
            Serializer: CertificateSimpleParentSerializer.
        """
        return CertificateSimpleParentSerializer

    def get_serializer_context(self):
        """Provide certificate type ID in serializer context.

        Returns:
            dict: Dictionary with 'type_id' key from nested router.
        """
        return {"type_id": self.kwargs.get('title_pk')}


class ParentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """API endpoint for retrieving parent/family relationship types (read-only).

    Provides list and detail endpoints for Parent (family relationship designation) models.
    """

    def get_queryset(self):
        """Return parent types ordered by ID.

        Returns:
            QuerySet: All Parent records ordered alphabetically by ID.
        """
        return Parent.objects.all().order_by("id")

    def get_serializer_class(self):
        """Return parent serializer.

        Returns:
            Serializer: ParentSerializer.
        """
        return ParentSerializer


class CertificateSinglePersonsViewSet(ModelViewSet):
    """API endpoint for managing single person records linked to certificates.

    Alternative person record format for specific certificate types.
    Only returns records for type ID 12; other type IDs return empty queryset.
    """

    def get_queryset(self):
        """Return single person records for the specified certificate type.

        Returns:
            QuerySet: CertificateSinglePerson records for type_id, empty for non-matching types.
        """
        type_id = int(self.kwargs.get('title_pk'))
        if type_id == 12:
            return CertificateSinglePerson.objects.optimized().filter(type_id=type_id).all()
        return CertificateSinglePerson.objects.optimized().filter(type_id=-1)

    def get_serializer_class(self):
        """Return single person serializer.

        Returns:
            Serializer: CertificateSinglePersonSerializer.
        """
        return CertificateSinglePersonSerializer

    def get_serializer_context(self):
        """Provide certificate type ID in serializer context.

        Returns:
            dict: Dictionary with 'type_id' key from nested router.
        """
        return {"type_id": self.kwargs.get('title_pk')}


class CertificateDatesViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """API endpoint for retrieving dates associated with certificates (read-only).

    Provides access to relevant dates (deadlines, etc.) linked to certificate types.
    """

    def get_queryset(self):
        """Return dates for the specified certificate type.

        Returns:
            QuerySet: CertificateDate records for the certificate type_id.
        """
        type_id = int(self.kwargs.get('title_pk'))
        return CertificateDate.objects.optimized().filter(type_id=type_id).all()

    def get_serializer_class(self):
        """Return certificate date serializer.

        Returns:
            Serializer: CertificateDateSerializer.
        """
        return CertificateDateSerializer

    def get_serializer_context(self):
        """Provide certificate type ID in serializer context.

        Returns:
            dict: Dictionary with 'type_id' key from nested router.
        """
        return {"type_id": self.kwargs.get('title_pk')}


class PersonBirthAddressViewSet(ModelViewSet):
    """API endpoint for managing birth address records.

    Provides full CRUD operations for PersonBirthAddress model with
    support for creating hierarchical location data (street, town, county, country).
    """
    queryset = PersonBirthAddress.objects.optimized().all()

    def get_serializer_class(self):
        """Select serializer based on request method.

        Returns:
            Serializer: PersonBirthAddressCreateSerializer for POST, PersonBirthAddressSerializer for GET.
        """
        if self.request.method == "POST":
            return PersonBirthAddressCreateSerializer
        return PersonBirthAddressSerializer


class CountysViewSet(ModelViewSet):
    """API endpoint for managing counties/administrative divisions.

    Provides full CRUD operations for County model with support for
    authenticated users to create/update and public read access.
    """
    queryset = County.objects.optimized().all().order_by("name")
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = Pagination300

    def get_serializer_class(self):
        """Select serializer based on request method.

        Returns:
            Serializer: CountyCreateSerializer for POST/PUT/PATCH, CountySerializer for GET.
        """
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return CountyCreateSerializer
        return CountySerializer


class TownViewSet(ModelViewSet):
    """API endpoint for managing towns/municipalities.

    Provides full CRUD operations for Town model with support for
    authenticated users to create/update and public read access.
    """
    queryset = Town.objects.optimized().all().order_by("name")
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = Pagination300

    def get_serializer_class(self):
        """Select serializer based on request method.

        Returns:
            Serializer: TownCreateSerializer for POST/PUT/PATCH, TownSerializer for GET.
        """
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return TownCreateSerializer
        return TownSerializer


class HouseViewSet(ModelViewSet):
    """API endpoint for managing house addresses.

    Provides full CRUD operations for House model (physical addresses)
    with support for authenticated users to create/update and public read access.
    """
    queryset = House.objects.optimized().all().order_by("street__name", "house_number")

    def get_serializer_class(self):
        """Select serializer based on request method.

        Returns:
            Serializer: HouseCreateSerializer for POST, HouseSerializer for GET.
        """
        if self.request.method == "POST":
            return HouseCreateSerializer
        return HouseSerializer


class PersonViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    GenericViewSet
):
    """API endpoint for managing person records (staff-only).

    Restricted to staff members. Provides full CRUD operations for Person model
    with support for filtering, searching, and ordering across multiple biographical fields.

    Search fields: name, surname, ID number, birth date.
    Ordering fields: name, ID number, birth date, ID issue date.
    """
    permission_classes = [IsStaff]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'surname', "id_number", "birth_date"]
    ordering_fields = ["name", "id_number", "birth_date", "id_issue_date"]

    def get_queryset(self):
        """Return optimized queryset of persons.

        Returns:
            QuerySet: All Person records with relations pre-fetched via select_related.
        """
        return Person.objects.optimized().all()

    def get_serializer_class(self):
        """Select serializer based on request method.

        Returns:
            Serializer: PersonCreateOrUpdateSerializer for POST/PUT, PersonSerializer for GET.
        """
        if self.request.method in ["POST", "PUT"]:
            return PersonCreateOrUpdateSerializer
        return PersonSerializer

    def get_serializer_context(self):
        """Provide person ID in serializer context.

        Returns:
            dict: Dictionary with 'id' key from URL parameters.
        """
        return {"id": self.kwargs.get('pk')}
