from certificates.classes.atestado_fifth import AtestadoFifth
from certificates.classes.atestado_one import AtestadoOne
from certificates.classes.atestado_second import AtestadoSecond
from certificates.classes.atestado_seventh import AtestadoSeventh
from certificates.classes.atestado_third import AtestadoThird
from certificates.classes.auto_construcao import AutoConstrucao
from certificates.classes.auto_enterro import AutoEnterro
from certificates.classes.auto_mod_coval import AutoModCovalAndLicBarraca
from certificates.classes.cert_compa_coval import CertCompraCoval
from certificates.classes.licenca_bufett import LicencaBufett
from certificates.classes.licenca_transladacao import LicencaTransladacao
from certificates.classes.string_helper import StringHelper
from datetime import date
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.db.transaction import atomic
from . import helpers
from .classes.document_data import DocumentData

from .models import (
    BiuldingType,
    Cemiterio,
    Certificate,
    CertificateData,
    CertificateDate,
    CertificateRange,
    CertificateSimpleParent,
    CertificateSimplePerson,
    CertificateSinglePerson,
    CertificateTitle,
    CertificateTypes,
    Change,
    Country,
    County,
    Coval,
    CovalSalles,
    House,
    IDType,
    Ifen,
    Instituition,
    Parent,
    Person,
    Customer,
    PersonBirthAddress,
    Street,
    Town,
    University,
)


def get_extra_kwargs(fields):
    return {
        field: {'style': {'base_template': 'input.html'}}
        for field in fields
        if field not in ['id', 'file']
    }


class CustomerSerializer(ModelSerializer):
    first_name = serializers.SerializerMethodField(method_name="get_first_name")
    last_name = serializers.SerializerMethodField(method_name="get_last_name")
    back_staff = serializers.SerializerMethodField(method_name="get_back_staff")

    class Meta:
        model = Customer
        fields = ["id", "user", "first_name", "last_name", "back_staff", "level"]

    def get_first_name(self, customer: Customer):
        return customer.user.first_name

    def get_back_staff(self, customer: Customer):
        return customer.backstaff

    def get_last_name(self, customer: Customer):
        return customer.user.last_name


class CountryCreateSerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name", "code"]

    def create(self, validate_data):
        name = validate_data.get('name')
        validate_data['slug'] = helpers.slugify(validate_data.get('name'))
        country = Country.objects.filter(name=name)
        if not country:
            return super().create(validate_data)
        return country.first()

    def update(self, instance, validate_data):
        name = validate_data.get('name')
        slug = validate_data['slug'] = helpers.slugify(name)
        code = validate_data['code']
        object = Country.objects.filter(slug=slug, code=code)
        if not object:
            return super().update(instance, validate_data)
        return object.first()


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name", "code"]


class CountyCreateSerializer(ModelSerializer):
    class Meta:
        model = County
        fields = ["id", "name", "country"]
        extra_kwargs = get_extra_kwargs(fields)

    def create(self, validate_data):
        name = validate_data.get('name')
        object_list = County.objects.optimized().filter(name=name)
        if object_list:
            return object_list.first()
        validate_data['slug'] = helpers.slugify(validate_data.get('name'))
        return super().create(validate_data)

    def update(self, instance, validate_data):
        name = validate_data.get('name')
        slug = validate_data['slug'] = helpers.slugify(name)
        country = validate_data['country']
        object = County.objects.optimized().filter(slug=slug, country=country)
        if not object:
            return super().update(instance, validate_data)
        return object.first()


class CountySerializer(ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = County
        fields = ["id", "name", "slug", "country"]


class UniversityCreateSerializer(ModelSerializer):
    class Meta:
        model = University
        fields = ["id", "name"]

    def create(self, validate_data):
        name = validate_data.get('name')
        object_list = University.objects.filter(name=name)
        if object_list:
            return object_list.first()
        return super().create(validate_data)


class UniversitySerializer(ModelSerializer):
    class Meta:
        model = University
        fields = ["id", "name"]


class BiuldingTypeSerializer(ModelSerializer):
    class Meta:
        model = BiuldingType
        fields = ["id", "name", "prefix"]


class TownCreateSerializer(ModelSerializer):
    class Meta:
        model = Town
        fields = ["id", "name", "county"]
        extra_kwargs = get_extra_kwargs(fields)

    def create(self, validate_data):
        name = validate_data.get('name')
        object_list = Town.objects.optimized().filter(name=name)
        if object_list:
            return object_list.first()
        validate_data['slug'] = helpers.slugify(validate_data.get('name'))
        return super().create(validate_data)

    def update(self, instance, validate_data):
        name = validate_data.get('name')
        slug = validate_data['slug'] = helpers.slugify(name)
        county = validate_data['county']
        object = Town.objects.optimized().filter(slug=slug, county=county)
        if not object:
            return super().update(instance, validate_data)
        return object.first()


class IfenSerializer(ModelSerializer):
    class Meta:
        model = Ifen
        fields = ["id", "name", "size"]


class IfenUpdateSerializer(ModelSerializer):
    class Meta:
        model = Ifen
        fields = ["id", "size"]


class TownSerializer(ModelSerializer):
    county = CountySerializer()
    country = serializers.SerializerMethodField(method_name="get_country")

    class Meta:
        model = Town
        fields = ["id", "name", "slug", "county", "country"]

    def get_country(self, town):
        return f"{town.county.country.name}"


class StreetCreateSerializer(ModelSerializer):
    class Meta:
        model = Street
        fields = ["id", "name", "town"]
        extra_kwargs = get_extra_kwargs(fields)

    def create(self, validate_data):
        name = validate_data.get('name')
        town = validate_data.get('town')
        object_list = Street.objects.optimized().filter(name=name, town=town)
        if object_list:
            return object_list.first()
        return super().create(validate_data)


class StreetSerializer(ModelSerializer):
    town = TownSerializer()

    class Meta:
        model = Street
        fields = ["id", "name", "town"]


class HouseSerializer(ModelSerializer):
    street = StreetSerializer()

    class Meta:
        model = House
        fields = ["id", "house_number", "street"]


class HouseCreateSerializer(ModelSerializer):
    house_number = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = House
        fields = ["id", "house_number", "street"]
        extra_kwargs = get_extra_kwargs(fields)

    def create(self, validate_data):
        house_number = validate_data.get('house_number')
        house = House.objects.optimized().filter(
            house_number=house_number,
            street_id=validate_data['street']
        )
        if not house:
            validate_data["house_number"] = house_number if (house_number != -1 or not house_number) else None
            return super().create(validate_data)
        return house.first()


class PersonBirthAddressSerializer(ModelSerializer):
    birth_street = StreetSerializer()
    birth_town = TownSerializer()
    birth_county = CountySerializer()
    birth_country = CountrySerializer()

    class Meta:
        model = PersonBirthAddress
        fields = ["id", "birth_street", "birth_town", "birth_county", "birth_country"]


def remove_duplicates_by_number(list_of_dicts):
    items_counts = {}
    dicts_to_remove = []
    for d in list_of_dicts:
        number = d.get("number")
        if number is not None:
            items_counts[number] = items_counts.get(number, 0) + 1
    for d in list_of_dicts:
        number = d.get("number")
        if number is not None and items_counts[number] > 1:
            dicts_to_remove.append(d)
    new_list = [d for d in list_of_dicts if d not in dicts_to_remove]
    return new_list


def remove_duplicates_keep_one(list_of_dicts, key_to_check):
    seen_values = set()
    new_list = []
    for d in list_of_dicts:
        value = d.get(key_to_check)
        if value is not None:
            if value not in seen_values:
                seen_values.add(value)
                new_list.append(d)
        else:
            new_list.append(d)
    return new_list


# def get_number(current_year, certificates, instance, type_id):
#     last = certificates.last()
#     if instance.type.certificate_type.id == int(last.type.certificate_type.id):
#         return instance.number
#     last_obj = None
#     if last is not None:
#         items = Certificate.objects.optimized().filter(type__certificate_type__id=last.type.certificate_type.id,
#                                                        date_issue__year=current_year, number__endswith=current_year)
#         if items.exists():
#             items = [item for item in items.values()]
#             last_obj = sorted(items, key=lambda item: int(item['number'].replace("-", "")), reverse=True)[0]
#     if last_obj is not None:
#         return f"{int(last_obj['number'].split('-')[0]) + 1}-{current_year}"
#     return f"1-{current_year}"

def get_number(current_year, certificates, instance, type_id):
    """
    Generate the next certificate number.
    Handles cases for both new certificates (create) and existing ones (update).
    """
    # 1. If instance exists and already has the correct type, keep the number (Update case)
    if instance and instance.type and instance.type.certificate_type:
        # Check if the type is the same to avoid re-numbering
        if int(instance.type.certificate_type.id) == int(type_id):
            return instance.number

    # 2. Look for the last certificate of this type in the current year
    last = certificates.last()
    last_obj = None

    if last is not None:
        # Filter items of the same group to find the highest sequence number
        items = Certificate.objects.optimized().filter(
            type__certificate_type__id=type_id,
            date_issue__year=current_year,
            number__endswith=str(current_year)
        )

        if items.exists():
            items_list = list(items.values('number'))
            # Sort by the numeric part before the hyphen
            last_obj = sorted(
                items_list,
                key=lambda item: int(item['number'].split('-')[0]),
                reverse=True
            )[0]

    # 3. Increment the number or start at 1
    if last_obj:
        next_seq = int(last_obj['number'].split('-')[0]) + 1
        return f"{next_seq}-{current_year}"

    return f"1-{current_year}"


def set_number(current_year, type_id):
    last = CertificateTitle.objects.optimized().get(id=type_id)
    last_obj = None
    if last is not None:
        items = Certificate.objects.optimized().filter(type__certificate_type__id=last.certificate_type.id,
                                                       date_issue__year=current_year, number__endswith=current_year)
        if items.exists():
            items = [item for item in items.values()]
            last_obj = sorted(items, key=lambda item: int(item['number'].replace("-", "")), reverse=True)[0]
    if last_obj is not None:
        return f"{int(last_obj['number'].split('-')[0]) + 1}-{current_year}"
    return f"1-{current_year}"


class PersonBirthAddressCreateSerializer(ModelSerializer):
    birth_street = serializers.PrimaryKeyRelatedField(
        queryset=Street.objects.optimized().all(), required=False, allow_null=True)
    birth_town = serializers.PrimaryKeyRelatedField(
        queryset=Town.objects.optimized().all(), required=False, allow_null=True)
    birth_county = serializers.PrimaryKeyRelatedField(
        queryset=County.objects.optimized().all(), required=False, allow_null=True)
    birth_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), required=True)

    class Meta:
        model = PersonBirthAddress
        fields = ["id", "birth_street", "birth_town", "birth_county", "birth_country"]

    def create(self, validate_data):
        street_instance = validate_data.get('birth_street', None)
        town_instance = validate_data.get('birth_town', None)
        county_instance = validate_data.get('birth_county', None)
        country_instance = validate_data['birth_country']
        street_id = street_instance.id if street_instance else None
        town_id = town_instance.id if town_instance else None
        county_id = county_instance.id if county_instance else None
        country_id = country_instance.id
        address = PersonBirthAddress.objects.optimized().filter(
            birth_street=street_id,
            birth_town=town_id,
            birth_county=county_id,
            birth_country=country_id,
        )
        if not address:
            return super().create(validate_data)
        return address.first()


# Move rules outside to make them accessible and reusable
PERSON_VALIDATION_RULES = {
    'birth_date': {'required': True, 'allow_null': False},
    'birth_address': {'required': True, 'allow_null': False},
    'id_issue_country': {'required': True, 'allow_null': False},
    'nationality': {'required': True, 'allow_null': False},
    'id_issue_date': {'required': True, 'allow_null': False},
    'id_expire_date': {'required': True, 'allow_null': False},
    'address': {'required': True, 'allow_null': False},
    'status': {'required': True, 'allow_null': False},
    'gender': {'required': True, 'allow_null': False},
}


class PersonCreateOrUpdateSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = [
            "id", "name", "surname", "birth_date", "birth_address", "id_type",
            "id_number", "id_issue_local", "id_issue_country", "nationality",
            "id_issue_date", "id_expire_date", "father_name", "mother_name",
            "address", "status", "gender",
        ]

        # Use the variable defined at the module level
        extra_kwargs = {
            field: {
                'style': {'base_template': 'input.html'},
                **PERSON_VALIDATION_RULES.get(field, {})
            }
            for field in fields
            if field not in ['id', 'file']
        }

    def validate(self, data):
        """
        Since you have existing NULL data, this method ensures
        NEW data or UPDATED data can never be saved as NULL.
        """
        # Parent validation (Father or Mother)
        # Check 'data' (new values) or 'self.instance' (existing values)
        father = data.get('father_name') or (self.instance.father_name if self.instance else None)
        mother = data.get('mother_name') or (self.instance.mother_name if self.instance else None)

        if not father and not mother:
            raise serializers.ValidationError(
                {"person": "The person must have a father or mother recorded."}
            )
        return data

    def create(self, validated_data):
        # Check for duplicates
        if Person.objects.filter(
            id_type=validated_data['id_type'],
            id_number=validated_data['id_number']
        ).exists():
            raise serializers.ValidationError({"person": "There is a person with same ID already registered"})

        # Your custom logic for parent names
        if not validated_data.get('father_name') and not validated_data.get('mother_name'):
            raise serializers.ValidationError({"person": "The person must have a father or mother"})

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Logic to check if the ID is being changed to one that already exists
        id_type = validated_data.get('id_type', instance.id_type)
        id_number = validated_data.get('id_number', instance.id_number)

        duplicate = Person.objects.filter(id_type=id_type, id_number=id_number).exclude(id=instance.id)
        if duplicate.exists():
            raise serializers.ValidationError({"person": "There is another person with same ID already registered"})

        if not validated_data.get('father_name') and not validated_data.get('mother_name'):
            raise serializers.ValidationError({"person": "The person must have a father or mother"})

        return super().update(instance, validated_data)


class IDTypeSerializer(ModelSerializer):
    class Meta:
        model = IDType
        fields = ["id", "name"]


class InstituitionCreateSerializer(ModelSerializer):
    class Meta:
        model = Instituition
        fields = ["id", "name"]

    def create(self, validate_data):
        name = validate_data.get('name')
        object_list = Instituition.objects.filter(name=name)
        if object_list:
            return object_list.first()
        return super().create(validate_data)


class InstituitionSerializer(ModelSerializer):
    class Meta:
        model = Instituition
        fields = ["id", "name"]


class PersonSerializer(ModelSerializer):
    birth_address = PersonBirthAddressSerializer()
    address = HouseSerializer()
    id_type = IDTypeSerializer()
    id_issue_local = InstituitionSerializer()
    id_issue_country = CountrySerializer()
    nationality = CountrySerializer()

    class Meta:
        model = Person
        fields = [
            "id", "name", "surname", "birth_date", "birth_address", "id_type",
            "id_number", "id_issue_local", "id_issue_country", "nationality",
            "id_issue_date", "id_expire_date", "father_name", "mother_name",
            "address", "status", "gender",
        ]


class BaseCertificateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(read_only=True)

    def validate(self, data):
        """Shared validation for all certificates."""
        if not data.get('main_person'):
            raise serializers.ValidationError(
                {"main_person": "You must provide a main person to issue a certificate."}
            )
        return data

    def _prepare_certificate_data(self, validated_data, instance=None):
        """Common logic to set numbering and type."""
        current_year = date.today().year
        type_id = int(self.context['type_id'])

        certificates = Certificate.objects.optimized().filter(
            type_id=type_id,
            date_issue__year=current_year
        )

        validated_data["number"] = get_number(current_year, certificates, instance, type_id)
        validated_data["type_id"] = type_id
        return validated_data

    def _finalize_certificate(self, certificate, validated_data, model_class):
        """Shared logic to render text and sync addresses."""
        main_person = validated_data["main_person"]

        # Prepare Document Data
        doc_data = DocumentData(
            main_person,
            validated_data,
            certificate,
            validated_data.get("secondary_person")
        )

        # Instantiate the specific Atestado model (AtestadoOne, AtestadoSecond, etc)
        document_model = model_class(doc_data)

        # Render and Update
        text, file_name, status = StringHelper.renderText(document_model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")

        # Update or Create CertificateData (house address)
        CertificateData.objects.update_or_create(
            certificate_id=certificate.id,
            defaults={'house': main_person.address}
        )


class CertificateModelOneCreateSerializer(BaseCertificateSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "house", "file"]
        extra_kwargs = get_extra_kwargs(fields)

    @atomic()
    def create(self, validated_data):

        validated_data = self._prepare_certificate_data(validated_data)
        certificate = super().create(validated_data)
        self._finalize_certificate(certificate, validated_data, AtestadoOne)
        certificate = Certificate.objects.optimized().get(id=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def update(self, instance, validated_data):
        validated_data = self._prepare_certificate_data(validated_data, instance)
        certificate = super().update(instance, validated_data)
        self._finalize_certificate(certificate, validated_data, AtestadoOne)
        certificate = Certificate.objects.optimized().get(id=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}


class CertificateModelTwoCreateSerializer(BaseCertificateSerializer):
    instituition = serializers.IntegerField()
    university = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "house", "instituition", "university", "file"]
        extra_kwargs = get_extra_kwargs(fields)

    def validate_instituition(self, value):
        if not Instituition.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid institution.")
        return value

    @atomic()
    def create(self, validated_data):
        # Capture the IDs sent in the request
        inst_id = validated_data.pop("instituition")
        univ_id = validated_data.pop("university", None)

        # Prepare numbering and type metadata
        validated_data = self._prepare_certificate_data(validated_data)
        certificate = super().create(validated_data)

        # FETCH THE ACTUAL INSTANCES (Objects) for rendering
        from certificates.models import Instituition, University
        instituition_obj = Instituition.objects.get(id=inst_id)
        university_obj = University.objects.get(id=univ_id) if univ_id else None

        # Add the objects back to the dictionary for DocumentData to process
        validated_data["instituition"] = instituition_obj
        validated_data["university"] = university_obj

        # Now the AtestadoSecond class will receive objects instead of integers
        self._finalize_certificate(certificate, validated_data, AtestadoSecond)

        # Return the IDs instead of objects in the API response
        validated_data["instituition"] = inst_id
        validated_data["university"] = univ_id
        certificate = Certificate.objects.optimized().get(id=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def update(self, instance, validated_data):
        """
        Updates the certificate and regenerates the rendered text.
        """
        # Capture the IDs sent in the request (removing them from model update dict)
        inst_id = validated_data.pop("instituition")
        univ_id = validated_data.pop("university", None)

        current_year = date.today().year

        # Prepare numbering (passes instance to keep current number if type hasn't changed)
        validated_data = self._prepare_certificate_data(validated_data, instance)

        # Perform the standard model update
        certificate = super().update(instance, validated_data)

        # FETCH THE ACTUAL INSTANCES (Objects) for document rendering
        # This ensures the atestado classes can access attributes like .name
        from certificates.models import Instituition, University
        instituition_obj = Instituition.objects.get(id=inst_id)
        university_obj = University.objects.get(id=univ_id) if univ_id else None

        # Add the objects back to validated_data for the rendering helper
        validated_data["instituition"] = instituition_obj
        validated_data["university"] = university_obj

        # Regenerate the certificate text using the second model class
        self._finalize_certificate(certificate, validated_data, AtestadoSecond)

        # Return the IDs instead of objects to match the API contract
        validated_data["instituition"] = inst_id
        validated_data["university"] = univ_id
        certificate = Certificate.objects.optimized().get(id=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}


class CertificateModelThreeCreateSerializer(BaseCertificateSerializer):
    date = serializers.DateField(allow_null=True, required=False)

    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "house", "date", "file"]
        extra_kwargs = get_extra_kwargs(fields)

    @atomic()
    def create(self, validated_data):
        """
        Creates a Type Three certificate and renders the document text.
        """
        # Remove 'date' if it's not a field in the Certificate model
        # to prevent errors during super().create()
        cert_date = validated_data.pop("date", None)

        # Prepare numbering and type metadata via base helper
        validated_data = self._prepare_certificate_data(validated_data)

        # Create the base Certificate instance
        certificate = super().create(validated_data)

        # Re-insert the date into validated_data so the AtestadoThird class can use it
        validated_data["date"] = cert_date

        # Finalize by rendering text (AtestadoThird) and syncing address
        self._finalize_certificate(certificate, validated_data, AtestadoThird)
        certificate = Certificate.objects.optimized().get(id=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def update(self, instance, validated_data):
        """
        Updates a Type Three certificate and regenerates the rendered text.
        """
        # Remove 'date' before updating the model instance
        cert_date = validated_data.pop("date", None)

        # Prepare metadata (passing instance to preserve number if applicable)
        validated_data = self._prepare_certificate_data(validated_data, instance)

        # Perform the standard model update
        certificate = super().update(instance, validated_data)

        # Re-insert the date for the rendering logic
        validated_data["date"] = cert_date

        # Regenerate document content and sync house address
        self._finalize_certificate(certificate, validated_data, AtestadoThird)
        certificate = Certificate.objects.optimized().get(id=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}


class CertificateModelFifthCreateSerializer(BaseCertificateSerializer):
    instituition = serializers.IntegerField()

    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "house", "instituition", "file"]
        extra_kwargs = get_extra_kwargs(fields)

    def validate_instituition(self, value):
        """Check if the institution exists before processing."""
        if not value:
            raise serializers.ValidationError("Please select an institution.")
        if not Instituition.objects.filter(id=value).exists():
            raise serializers.ValidationError("The selected institution is invalid.")
        return value

    def validate(self, data):
        """
        Custom validation for Type 12 certificates regarding person availability.
        """
        # Call the base validation (main_person check)
        super().validate(data)

        type_id = int(self.context.get('type_id', 0))
        if type_id == 12:
            # Check if required associated persons exist for this specific type
            if not CertificateSimplePerson.objects.filter(type_id=12).exists():
                print("No simple persons found for type 12")
                raise serializers.ValidationError({'persons': "No simple persons found for this type."})
            if not CertificateSinglePerson.objects.filter(type_id=12).exists():
                print("No single person found for type 12")
                raise serializers.ValidationError({'persons': "No single person found for this type."})
        return data

    @atomic()
    def create(self, validated_data):
        """
        Creates a Type Five certificate and renders document text.
        """
        # Capture the ID and remove it from model creation data
        inst_id = validated_data.pop("instituition")

        # Prepare metadata (numbering/type)
        validated_data = self._prepare_certificate_data(validated_data)
        certificate = super().create(validated_data)

        # FETCH THE ACTUAL INSTANCE for the rendering engine
        from certificates.models import Instituition
        instituition_obj = Instituition.objects.get(id=inst_id)

        # Inject object into data dictionary for AtestadoFifth
        validated_data["instituition"] = instituition_obj

        # Finalize (Render text and sync house address)
        self._finalize_certificate(certificate, validated_data, AtestadoFifth)

        # Re-set ID for the final response
        validated_data["instituition"] = inst_id
        certificate = Certificate.objects.optimized().get(id=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def update(self, instance, validated_data):
        """
        Updates a Type Five certificate and regenerates document text.
        """
        # Capture ID and remove from model update data
        inst_id = validated_data.pop("instituition")

        # Prepare metadata (passing instance to preserve current number)
        validated_data = self._prepare_certificate_data(validated_data, instance)

        # Update the Certificate record
        certificate = super().update(instance, validated_data)

        # FETCH THE ACTUAL INSTANCE
        from certificates.models import Instituition
        instituition_obj = Instituition.objects.get(id=inst_id)

        # Inject object for the helper
        validated_data["instituition"] = instituition_obj

        # Finalize rendering using AtestadoFifth logic
        self._finalize_certificate(certificate, validated_data, AtestadoFifth)

        # Restore ID for the response
        validated_data["instituition"] = inst_id
        certificate = Certificate.objects.optimized().get(id=certificate.id)

        return {**validated_data, "id": certificate.id, "file": certificate.file}


class CovalSerializer(ModelSerializer):
    class Meta:
        model = Coval
        fields = ["id", "nick_number", "number", "name", "date_used", "closed", "selled"]


class CemiterioSerializer(ModelSerializer):
    class Meta:
        model = Cemiterio
        fields = ["id", "name", "county"]


class ChangeSerializer(ModelSerializer):
    class Meta:
        model = Change
        fields = ["id", "name"]


class CertificateModelEnterroCreateSerializer(BaseCertificateSerializer):
    cemiterio = serializers.IntegerField()
    died_date = serializers.DateField()
    entero_date = serializers.DateField()

    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "cemiterio", "died_date", "entero_date", "file"]
        extra_kwargs = get_extra_kwargs(fields)

    def validate_cemiterio(self, value):
        from certificates.models import Cemiterio
        if not value:
            raise serializers.ValidationError("Please select a cemetery.")
        if not Cemiterio.objects.filter(id=value).exists():
            raise serializers.ValidationError("The selected cemetery is invalid.")
        return value

    def _process_burial_logic(self, certificate, validated_data, type_id):
        from certificates.models import Cemiterio, Coval, CertificateSinglePerson

        cemiterio = Cemiterio.objects.get(id=validated_data["cemiterio"])
        today = date.today()

        # 1. Find available graves (older than 1 year and not closed)
        available_covals = Coval.objects.filter(
            date_used__year__lt=(today.year - 1),
            closed=False,
            cemiterio=cemiterio
        ).order_by("square", "date_used")

        if not available_covals.exists():
            raise serializers.ValidationError({'cemiterio': 'There is no space available.'})

        # 2. Get deceased person details
        person_details = CertificateSinglePerson.objects.filter(type_id=type_id).first()
        if not person_details:
            raise serializers.ValidationError({'coval': 'Missing deceased person details.'})

        # 3. Recycle plot logic
        old_coval = available_covals.first()
        old_coval.closed = True
        old_coval.save()

        # 4. Create new grave record
        square_count = Coval.objects.filter(square=old_coval.square).count()
        new_coval = Coval.objects.create(
            number=f"{square_count + 1}-{today.year} {old_coval.square}",
            nick_number=old_coval.nick_number,
            name=person_details.name,
            gender=person_details.gender,
            date_used=validated_data['entero_date'],
            date_of_deth=validated_data['died_date'],
            square=old_coval.square,
            cemiterio=cemiterio
        )

        # CRITICAL: Match the keys expected by AutoEnterro class
        validated_data["coval"] = new_coval
        validated_data["last_coval"] = old_coval
        validated_data["cemiterio"] = cemiterio

        # Finalize rendering
        self._finalize_certificate(certificate, validated_data, AutoEnterro)

    @atomic()
    def create(self, validated_data):
        # Pop extra fields
        cemiterio_id = validated_data.pop("cemiterio")
        died_date = validated_data.pop("died_date")
        entero_date = validated_data.pop("entero_date")
        type_id = int(self.context['type_id'])

        # Prepare base certificate
        validated_data = self._prepare_certificate_data(validated_data)
        certificate = super().create(validated_data)

        # Execute burial business logic
        validated_data.update({
            "cemiterio": cemiterio_id,
            "died_date": died_date,
            "entero_date": entero_date
        })
        self._process_burial_logic(certificate, validated_data, type_id)

        # Return original IDs for response
        validated_data["cemiterio"] = cemiterio_id
        certificate = Certificate.objects.optimized().get(id=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def update(self, instance, validated_data):
        cemiterio_id = validated_data.pop("cemiterio")
        died_date = validated_data.pop("died_date")
        entero_date = validated_data.pop("entero_date")
        type_id = int(self.context['type_id'])

        validated_data = self._prepare_certificate_data(validated_data, instance)
        certificate = super().update(instance, validated_data)

        validated_data.update({
            "cemiterio": cemiterio_id,
            "died_date": died_date,
            "entero_date": entero_date
        })
        self._process_burial_logic(certificate, validated_data, type_id)

        validated_data["cemiterio"] = cemiterio_id
        certificate = Certificate.objects.optimized().get(id=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}


class CertificateModelCertCompraCovalCreateSerializer(BaseCertificateSerializer):
    coval = serializers.IntegerField()

    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "coval", "file"]
        extra_kwargs = get_extra_kwargs(fields)

    def validate_coval(self, value):
        from certificates.models import Coval, CovalSalles
        if not value:
            raise serializers.ValidationError("Please select a coval.")

        coval_obj = Coval.objects.filter(id=value).first()
        if not coval_obj:
            raise serializers.ValidationError("This coval is not valid.")

        # Check specific business rules
        if coval_obj.date_of_deth is None:
            raise serializers.ValidationError("Cannot process a coval with an empty death date.")

        if CovalSalles.objects.filter(coval_id=value).exists():
            raise serializers.ValidationError("This coval has already been sold.")

        return value

    def _handle_coval_business_logic(self, certificate, validated_data, type_id):
        """
        Handles conditional rendering class selection and
        Coval sales state updates.
        """
        from certificates.models import Coval, CovalSalles
        coval_obj = Coval.objects.get(id=validated_data["coval"])

        # Determine which Rendering Model to use
        render_class = None
        if type_id == 24:
            # Side effect: Mark as sold and record the sale
            coval_obj.selled = True
            coval_obj.save()
            CovalSalles.objects.get_or_create(
                coval=coval_obj,
                person=validated_data["main_person"]
            )
            render_class = CertCompraCoval
        elif type_id == 30:
            render_class = LicencaTransladacao

        # Inject the actual object for the Rendering Engine
        validated_data["coval"] = coval_obj

        # Use base helper to finalize text and house address
        self._finalize_certificate(certificate, validated_data, render_class)

    @atomic()
    def create(self, validated_data):
        coval_id = validated_data.pop("coval")
        type_id = int(self.context['type_id'])

        # Base preparation
        validated_data = self._prepare_certificate_data(validated_data)
        certificate = super().create(validated_data)

        # Handle side effects and rendering
        validated_data["coval"] = coval_id
        self._handle_coval_business_logic(certificate, validated_data, type_id)

        # Restore ID for response
        validated_data["coval"] = coval_id
        certificate = Certificate.objects.optimized().get(id=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def update(self, instance, validated_data):
        coval_id = validated_data.pop("coval")
        type_id = int(self.context['type_id'])

        validated_data = self._prepare_certificate_data(validated_data, instance)
        certificate = super().update(instance, validated_data)

        validated_data["coval"] = coval_id
        self._handle_coval_business_logic(certificate, validated_data, type_id)

        validated_data["coval"] = coval_id
        certificate = Certificate.objects.optimized().get(id=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}


class CertificateModelAutoModCovalCreateSerializer(BaseCertificateSerializer):
    coval = serializers.IntegerField()
    change = serializers.IntegerField()

    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "coval", "change", "file"]
        extra_kwargs = get_extra_kwargs(fields)

    @atomic()
    def create(self, validated_data):
        # 1. Pop IDs to keep validated_data clean for model creation
        coval_id = validated_data.pop("coval")
        change_id = validated_data.pop("change")

        # 2. Prepare base certificate data (numbering/type)
        validated_data = self._prepare_certificate_data(validated_data)
        certificate = super().create(validated_data)

        # 3. Fetch objects for the document rendering engine
        from certificates.models import Coval, Change
        coval_obj = Coval.objects.get(id=coval_id)
        change_obj = Change.objects.get(id=change_id)

        # 4. Inject objects back for the helper to use
        validated_data["coval"] = coval_obj
        validated_data["change"] = change_obj

        # 5. Finalize rendering (uses AutoModCovalAndLicBarraca)
        self._finalize_certificate(certificate, validated_data, AutoModCovalAndLicBarraca)

        # 6. Restore IDs for the response context
        validated_data["coval"] = coval_id
        validated_data["change"] = change_id
        certificate = Certificate.objects.optimized().get(id=certificate.id)

        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def update(self, instance, validated_data):
        coval_id = validated_data.pop("coval")
        change_id = validated_data.pop("change")

        validated_data = self._prepare_certificate_data(validated_data, instance)
        certificate = super().update(instance, validated_data)

        from certificates.models import Coval, Change
        validated_data["coval"] = Coval.objects.get(id=coval_id)
        validated_data["change"] = Change.objects.get(id=change_id)

        self._finalize_certificate(certificate, validated_data, AutoModCovalAndLicBarraca)

        validated_data["coval"] = coval_id
        validated_data["change"] = change_id
        certificate = Certificate.objects.optimized().get(id=certificate.id)

        return {**validated_data, "id": certificate.id, "file": certificate.file}


class CertificateModelLicBarracaCreateSerializer(BaseCertificateSerializer):
    object = serializers.CharField()
    street = serializers.IntegerField()
    range = serializers.CharField()

    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "object", "street", "file", "range"]
        extra_kwargs = get_extra_kwargs(fields)

    def validate_object(self, value):
        if not value:
            raise serializers.ValidationError("Please type the object.")
        return value

    def validate_street(self, value):
        if not value:
            raise serializers.ValidationError("Please select a street.")
        from certificates.models import Street
        if not Street.objects.filter(id=value).exists():
            raise serializers.ValidationError("The selected street is invalid.")
        return value

    def _prepare_barraca_metadata(self, validated_data):
        """
        Helper to fetch actual model objects for Street and Range
        before document rendering.
        """
        from certificates.models import Street, CertificateRange

        # Fetch Street object
        street_id = validated_data.get("street")
        validated_data["street"] = Street.objects.filter(id=street_id).first()

        # Handle CertificateRange if type is 27
        type_id = int(self.context.get('type_id', 0))
        if type_id == 27:
            range_input = validated_data.get("range")
            # Logic: If it's a digit, search by ID. If it's a string, search by type.
            if str(range_input).isdigit():
                range_obj = CertificateRange.objects.filter(id=range_input).first()
            else:
                range_obj = CertificateRange.objects.filter(type=range_input).first()

            validated_data["range"] = range_obj

        return validated_data

    @atomic()
    def create(self, validated_data):
        # 1. Pop non-model fields
        obj_val = validated_data.pop("object")
        street_id = validated_data.pop("street")
        range_val = validated_data.pop("range")

        # 2. Base preparation (numbering/type)
        validated_data = self._prepare_certificate_data(validated_data)
        certificate = super().create(validated_data)

        # 3. Re-inject and resolve objects for rendering
        validated_data["object"] = obj_val
        validated_data["street"] = street_id
        validated_data["range"] = range_val
        validated_data = self._prepare_barraca_metadata(validated_data)

        # 4. Finalize rendering (uses AutoModCovalAndLicBarraca)
        self._finalize_certificate(certificate, validated_data, AutoModCovalAndLicBarraca)

        # 5. Restore original ID for response
        validated_data["street"] = street_id
        if hasattr(validated_data.get("range"), "type"):
            validated_data["range"] = range_val

        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def update(self, instance, validated_data):
        obj_val = validated_data.pop("object")
        street_id = validated_data.pop("street")
        range_val = validated_data.pop("range")

        validated_data = self._prepare_certificate_data(validated_data, instance)
        certificate = super().update(instance, validated_data)

        validated_data["object"] = obj_val
        validated_data["street"] = street_id
        validated_data["range"] = range_val
        validated_data = self._prepare_barraca_metadata(validated_data)

        self._finalize_certificate(certificate, validated_data, AutoModCovalAndLicBarraca)

        validated_data["street"] = street_id
        if hasattr(validated_data.get("range"), "type"):
            validated_data["range"] = range_val

        return {**validated_data, "id": certificate.id, "file": certificate.file}


class CertificateModelAutoConstrucaoCreateSerializer(BaseCertificateSerializer):
    building_type = serializers.IntegerField()
    street = serializers.IntegerField()

    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "building_type", "street", "file"]
        extra_kwargs = get_extra_kwargs(fields)

    def validate_building_type(self, value):
        """Validate that the building type exists."""
        if not value:
            raise serializers.ValidationError("Please select a building type.")
        # Note: Corrected typo 'BiuldingType' to match your original code
        if not BiuldingType.objects.filter(id=value).exists():
            raise serializers.ValidationError("The selected building type is invalid.")
        return value

    def validate_street(self, value):
        """Validate that the street exists."""
        if not value:
            raise serializers.ValidationError("Please select a street.")
        if not Street.objects.filter(id=value).exists():
            raise serializers.ValidationError("The selected street is invalid.")
        return value

    @atomic()
    def create(self, validated_data):
        """
        Creates a Construction Authorization certificate and renders document text.
        """
        # Capture IDs and remove them from model creation data
        building_id = validated_data.pop("building_type")
        street_id = validated_data.pop("street")

        # Prepare metadata (numbering and type) via base helper
        validated_data = self._prepare_certificate_data(validated_data)
        certificate = super().create(validated_data)

        # FETCH THE ACTUAL INSTANCES for the rendering engine
        # This prevents 'int' object has no attribute errors in AutoConstrucao class
        from certificates.models import BiuldingType, Street
        building_obj = BiuldingType.objects.get(id=building_id)
        street_obj = Street.objects.get(id=street_id)

        # Inject objects into data dictionary for the Document Model
        validated_data["building_type"] = building_obj
        validated_data["street"] = street_obj

        # Finalize (Render text using AutoConstrucao and sync house address)
        self._finalize_certificate(certificate, validated_data, AutoConstrucao)

        # Re-set IDs for the final JSON response
        validated_data["building_type"] = building_id
        validated_data["street"] = street_id

        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def update(self, instance, validated_data):
        """
        Updates a Construction Authorization certificate and regenerates text.
        """
        # Capture IDs and remove from model update data
        building_id = validated_data.pop("building_type")
        street_id = validated_data.pop("street")

        # Prepare metadata (preserving current number if applicable)
        validated_data = self._prepare_certificate_data(validated_data, instance)

        # Update the Certificate record
        certificate = super().update(instance, validated_data)

        # FETCH THE ACTUAL INSTANCES
        from certificates.models import BiuldingType, Street
        building_obj = BiuldingType.objects.get(id=building_id)
        street_obj = Street.objects.get(id=street_id)

        # Inject objects for the rendering logic
        validated_data["building_type"] = building_obj
        validated_data["street"] = street_obj

        # Regenerate document content using AutoConstrucao logic
        self._finalize_certificate(certificate, validated_data, AutoConstrucao)

        # Restore IDs for the response
        validated_data["building_type"] = building_id
        validated_data["street"] = street_id

        return {**validated_data, "id": certificate.id, "file": certificate.file}


class CertificateModelSeventhCreateSerializer(BaseCertificateSerializer):
    years = serializers.IntegerField()
    country = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "house", "years", "country", "file"]
        extra_kwargs = get_extra_kwargs(fields)

    def validate_years(self, value):
        if value is None or value < 0:
            raise serializers.ValidationError("Please provide a valid number of years.")
        return value

    def _resolve_country(self, validated_data):
        """
        Helper to fetch the actual Country model instance
        to satisfy the rendering engine requirements.
        """
        from certificates.models import Country
        country_id = validated_data.get("country")

        if country_id:
            # We fetch the object so AtestadoSeventh can access country.name
            country_obj = Country.objects.filter(id=country_id).first()
            validated_data["country"] = country_obj
        else:
            validated_data["country"] = None

        return validated_data

    @atomic()
    def create(self, validated_data):
        # 1. Pop fields not present in the Certificate model
        years = validated_data.pop("years")
        country_id = validated_data.pop("country", None)

        # 2. Prepare metadata (numbering, type_id) via base class
        validated_data = self._prepare_certificate_data(validated_data)
        certificate = super().create(validated_data)

        # 3. Re-inject data and resolve the Country object for rendering
        validated_data["years"] = years
        validated_data["country"] = country_id
        validated_data = self._resolve_country(validated_data)

        # 4. Finalize rendering (uses AtestadoSeventh) and sync address
        self._finalize_certificate(certificate, validated_data, AtestadoSeventh)

        # 5. Restore the integer ID for the final response
        validated_data["country"] = country_id

        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def update(self, instance, validated_data):
        years = validated_data.pop("years")
        country_id = validated_data.pop("country", None)

        # Prepare metadata (preserving existing number if applicable)
        validated_data = self._prepare_certificate_data(validated_data, instance)
        certificate = super().update(instance, validated_data)

        # Re-inject and resolve objects
        validated_data["years"] = years
        validated_data["country"] = country_id
        validated_data = self._resolve_country(validated_data)

        # Finalize rendering
        self._finalize_certificate(certificate, validated_data, AtestadoSeventh)

        # Restore ID for response
        validated_data["country"] = country_id

        return {**validated_data, "id": certificate.id, "file": certificate.file}


class CertificateModelLicencaBuffetCreateSerializer(BaseCertificateSerializer):
    infra = serializers.CharField()
    street = serializers.IntegerField()
    metros = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "infra", "street", "metros", "file"]
        extra_kwargs = get_extra_kwargs(fields)

    def _get_buffet_metadata(self, validated_data):
        """
        Helper to fetch Street objects and CertificateDate metadata
        required specifically for Buffet Licenses.
        """
        from certificates.models import Street, CertificateDate
        type_id = int(self.context['type_id'])

        # Fetch the Street object to avoid 'int' attribute errors during rendering
        street_id = validated_data.get("street")
        street_obj = Street.objects.filter(id=street_id).first()

        # Fetch date metadata required by the LicencaBufett class
        date_qs = CertificateDate.objects.optimized().filter(type_id=type_id).order_by('-date')
        last_date_obj = date_qs.first()

        validated_data["street"] = street_obj
        validated_data["dates"] = date_qs
        validated_data["last_date"] = last_date_obj.date if last_date_obj else None

        return validated_data

    @atomic()
    def create(self, validated_data):
        """
        Creates a Buffet License and renders document text.
        """
        # Pop non-model fields
        infra = validated_data.pop("infra")
        street_id = validated_data.pop("street")
        metros = validated_data.pop("metros", None)

        # Prepare metadata (numbering/type)
        validated_data = self._prepare_certificate_data(validated_data)
        certificate = super().create(validated_data)

        # Re-inject data and fetch objects for rendering
        validated_data["infra"] = infra
        validated_data["street"] = street_id
        validated_data["metros"] = metros
        validated_data = self._get_buffet_metadata(validated_data)

        # Finalize (Render text using LicencaBufett and sync address)
        self._finalize_certificate(certificate, validated_data, LicencaBufett)

        # Return IDs in the response
        validated_data["street"] = street_id

        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def update(self, instance, validated_data):
        """
        Updates a Buffet License and regenerates document text.
        """
        # Pop non-model fields
        infra = validated_data.pop("infra")
        street_id = validated_data.pop("street")
        metros = validated_data.pop("metros", None)

        # Prepare metadata (preserving current number)
        validated_data = self._prepare_certificate_data(validated_data, instance)
        certificate = super().update(instance, validated_data)

        # Re-inject data and fetch objects for rendering
        validated_data["infra"] = infra
        validated_data["street"] = street_id
        validated_data["metros"] = metros
        validated_data = self._get_buffet_metadata(validated_data)

        # Finalize rendering
        self._finalize_certificate(certificate, validated_data, LicencaBufett)

        # Return IDs in the response
        validated_data["street"] = street_id

        return {**validated_data, "id": certificate.id, "file": certificate.file}


class CertificateTypesSerializer(ModelSerializer):
    class Meta:
        model = CertificateTypes
        fields = ["id", "name", "gender", "slug"]


class CertificateTitleSerializer(ModelSerializer):
    certificate_type = CertificateTypesSerializer()

    class Meta:
        model = CertificateTitle
        fields = ["id", "certificate_type", "type_price", "name", "goal"]


class CovalSetUpSerializer(ModelSerializer):
    done = serializers.BooleanField(read_only=True)

    class Meta:
        model = Coval
        fields = ["id", "done"]

    def create(self, validate_data):
        covals = Coval.objects.order_by("square", "date_used")
        if not covals.exists():
            return {"done": True}
        count = 1
        square = covals[0].square
        for coval in covals:
            if coval.square != square:
                square = coval.square
                count = 1
            coval.number = f"{count}-{coval.date_used.year} {coval.square}"
            coval.save()
            count += 1
        return {"done": True}


class CertificateSimplePersonSerializer(ModelSerializer):
    type = CertificateTitleSerializer(read_only=True)

    class Meta:
        model = CertificateSimplePerson
        fields = ["id", "name", "birth_date", "gender", "type"]

    def create(self, validate_data):
        validate_data["type_id"] = int(self.context['type_id'])
        return super().create(validate_data)


class CertificateSimplePersonReadOnlySerializer(ModelSerializer):
    type = serializers.CharField(read_only=True)

    class Meta:
        model = CertificateSimplePerson
        fields = ["id", "name", "birth_date", "gender", "type"]

    def create(self, validate_data):
        validate_data["type_id"] = int(self.context['type_id'])
        return super().create(validate_data)


class CertificateSimpleParentSerializer(ModelSerializer):
    type = CertificateTitleSerializer(read_only=True)

    class Meta:
        model = CertificateSimpleParent
        fields = ["id", "name", "birth_date", "parent", "type"]

    def create(self, validate_data):
        validate_data["type_id"] = int(self.context['type_id'])
        return super().create(validate_data)


class ParentSerializer(ModelSerializer):
    class Meta:
        model = Parent
        fields = ["id", "title"]


class CertificateDateSerializer(ModelSerializer):
    type = CertificateTitleSerializer(read_only=True)

    class Meta:
        model = CertificateDate
        fields = ["id", "date", "type"]

    def create(self, validate_data):
        validate_data["type_id"] = int(self.context['type_id'])
        return super().create(validate_data)


class CertificateSinglePersonSerializer(ModelSerializer):
    type = CertificateTitleSerializer(read_only=True)

    class Meta:
        model = CertificateSinglePerson
        fields = ["id", "name", "gender", "type"]

    def create(self, validate_data):
        CertificateSinglePerson.objects.optimized().filter(type_id=self.context['type_id']).delete()
        validate_data["type_id"] = int(self.context['type_id'])
        return super().create(validate_data)


class CertificateSerializer(ModelSerializer):
    type = CertificateTitleSerializer()
    main_person = PersonSerializer()
    secondary_person = PersonSerializer()
    house = HouseSerializer()
    status_detail = serializers.SerializerMethodField(method_name="get_status_detail")

    class Meta:
        model = Certificate
        fields = [
            "id", "type", "number", "main_person", "secondary_person", "date_issue",
            "file", "text", "house", "status", "status_detail", "obs",
        ]

    def get_status_detail(self, certificate: Certificate):
        mapping = {"R": "Revisto", "C": "Concluído", "F": "Incorrecto", "A": "Arquivado"}
        return mapping.get(certificate.status, "Pendente")


class CertificateCommentSerializer(ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "obs"]


class CertificateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "status"]


class MetadataSerializer(serializers.Serializer):
    countries = CountrySerializer(many=True)
    universities = UniversitySerializer(many=True)
    ifens = IfenSerializer(many=True)
    buildings = BiuldingTypeSerializer(many=True)
    cemiterios = CemiterioSerializer(many=True)
    streets = StreetSerializer(many=True)
    changes = ChangeSerializer(many=True)
    towns = TownSerializer(many=True)
    countys = CountySerializer(many=True)
    certificateTitles = CertificateTitleSerializer(many=True)
    covals = CovalSerializer(many=True)
    idtypes = IDTypeSerializer(many=True)
    intituitions = InstituitionSerializer(many=True)
