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

    def create(self, validate_data):
        name = validate_data.get('name')
        object_list = County.objects.filter(name=name)
        if object_list:
            return object_list.first()
        validate_data['slug'] = helpers.slugify(validate_data.get('name'))
        return super().create(validate_data)
        
    def update(self, instance, validate_data):
        name = validate_data.get('name')
        slug = validate_data['slug'] = helpers.slugify(name)
        country = validate_data['country']
        object = County.objects.filter(slug=slug, country=country)
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

    def create(self, validate_data):
        name = validate_data.get('name')
        object_list = Town.objects.filter(name=name)
        if object_list:
            return object_list.first()
        validate_data['slug'] = helpers.slugify(validate_data.get('name'))
        return super().create(validate_data)
    
    def update(self, instance, validate_data):
        name = validate_data.get('name')
        slug = validate_data['slug'] = helpers.slugify(name)
        county = validate_data['county']
        object = Town.objects.filter(slug=slug, county=county)
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

    def create(self, validate_data):
        name = validate_data.get('name')
        town = validate_data.get('town')
        object_list = Street.objects.filter(name=name, town=town)
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

    def create(self, validate_data):
        house_number = validate_data.get('house_number')
        house = House.objects.filter(
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

def get_number(current_year, certificates, instance, type_id):
    last = certificates.last()
    if instance.type.certificate_type.id == int(last.type.certificate_type.id):
        return instance.number
    last_obj = None
    if last != None:
        items = Certificate.objects.filter(type__certificate_type__id = last.type.certificate_type.id, date_issue__year=current_year, number__endswith=current_year)
        if items.exists():
            items = [item for item in items.values()]
            last_obj = sorted(items, key=lambda item:int(item['number'].replace("-","") ), reverse=True)[0]
    if last_obj != None:
        return f"{int(last_obj['number'].split('-')[0]) + 1}-{current_year}"
    return f"1-{current_year}"

def set_number(current_year, type_id):
    last = CertificateTitle.objects.get(id=type_id)
    last_obj = None
    if last != None:
        items = Certificate.objects.filter(type__certificate_type__id = last.certificate_type.id, date_issue__year=current_year, number__endswith=current_year)
        if items.exists():
            items = [item for item in items.values()]
            last_obj = sorted(items, key=lambda item:int(item['number'].replace("-","") ), reverse=True)[0]
    if last_obj != None:
        return f"{int(last_obj['number'].split('-')[0]) + 1}-{current_year}"
    return f"1-{current_year}"

class PersonBirthAddressCreateSerializer(ModelSerializer):
    birth_street = serializers.PrimaryKeyRelatedField(queryset=Street.objects.all(), required=False, allow_null=True)
    birth_town = serializers.PrimaryKeyRelatedField(queryset=Town.objects.all(), required=False, allow_null=True)
    birth_county = serializers.PrimaryKeyRelatedField(queryset=County.objects.all(), required=False, allow_null=True)
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
        address = PersonBirthAddress.objects.filter(
            birth_street=street_id,
            birth_town=town_id,
            birth_county=county_id,
            birth_country=country_id,
        )
        if not address:
            return super().create(validate_data)
        return address.first()

class PersonCreateOrUpdateSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = [
            "id", "name", "surname", "birth_date", "birth_address", "id_type",
            "id_number", "id_issue_local", "id_issue_country", "nationality",
            "id_issue_date", "id_expire_date", "father_name", "mother_name",
            "address", "status", "gender",
        ]

    def create(self, validate_data):
        person = Person.objects.filter(id_type=validate_data['id_type'], id_number=validate_data['id_number'])
        if not validate_data['father_name'] and not validate_data['mother_name']:
            raise serializers.ValidationError({"person": "The person must to have a father or mother"})
        if not person:
            return super().create(validate_data)
        raise serializers.ValidationError({"person": "There is a person with same ID already registered"})

    def update(self, instance, validate_data):
        person = Person.objects.filter(id=self.context['id'])
        if not validate_data['father_name'] and not validate_data['mother_name']:
            raise serializers.ValidationError({"person": "The person must to have a father or mother"})
        if person.first().id == instance.id:
            return super().update(instance, validate_data)
        raise serializers.ValidationError({"person": "There is a person with same ID already registered"})

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

class CertificateModelOneCreateSerializer(ModelSerializer):
    file = serializers.FileField(read_only=True)
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "house", "file"]

    @atomic()
    def update(self, instance, validated_data):
        current_year = date.today().year
        certificates = Certificate.objects.filter(type_id=self.context['type_id'], date_issue__year=current_year)
        validated_data["number"] = get_number(current_year, certificates, instance, self.context['type_id'])
        validated_data["type_id"] = int(self.context['type_id'])
        certificate = super().update(instance, validated_data)
        model = AtestadoOne(DocumentData(validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.filter(pk=certificate.id).update(house=validated_data["main_person"].address)
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):
        current_year = date.today().year
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = int(self.context['type_id'])
        new_validate_data = validate_data.copy()
        certificate = super().create(new_validate_data)
        model = AtestadoOne(DocumentData(validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.create(certificate_id=certificate.id, house=validate_data["main_person"].address)
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validate_data, "id": certificate.id, "file": certificate.file}

class CertificateModelOneSerializer(ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "house_id", "file"]

class CertificateModelTwoCreateSerializer(ModelSerializer):
    instituition = serializers.IntegerField()
    university = serializers.IntegerField(allow_null=True)
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "house", "instituition", "university", "file"]

    def validate_institution(self, institution):
        if not institution:
            raise serializers.ValidationError({'institution': "Select instituition"})
        elif not Instituition.objects.filter(id=institution).exists():
            raise serializers.ValidationError({'institution': "This instituition is not valid"})
        return institution

    def validate_university(self, university):
        if university and not University.objects.filter(id=university).exists():
            raise serializers.ValidationError({'university': "This university is not valid"})
        return university

    @atomic()
    def update(self, instance, validated_data):                              
        current_year = date.today().year
        certificates = Certificate.objects.filter(type_id=self.context['type_id'], date_issue__year=current_year)
        validated_data["number"] = get_number(current_year, certificates, instance, self.context['type_id'])
        type_id = validated_data["type_id"] = int(self.context['type_id'])
        validated_data["status"] = "P"
        new_validate_data = validated_data.copy()
        del new_validate_data["instituition"]
        del new_validate_data["university"]
        certificate = super().update(instance, new_validate_data)
        instituition = Instituition.objects.filter(id=validated_data["instituition"]).first()
        if type_id == 3:
            university = University.objects.filter(id=validated_data["university"]).first()
        model = AtestadoSecond(DocumentData(validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.filter(pk=certificate.id).update(house=validated_data["main_person"].address)
        validated_data["instituition"] = instituition.id
        if type_id == 3:
            validated_data["university"] = university.id
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):
        current_year = date.today().year
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        type_id = validate_data["type_id"] = int(self.context['type_id'])
        new_validate_data = validate_data.copy()
        del new_validate_data["instituition"]
        del new_validate_data["university"]
        certificate = super().create(new_validate_data)
        instituition = Instituition.objects.filter(id=validate_data["instituition"]).first()
        if type_id == 3:
            university = University.objects.filter(id=validate_data["university"]).first()
        model = AtestadoSecond(DocumentData(validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.create(certificate_id=certificate.id, house=validate_data["main_person"].address)
        validate_data["instituition"] = instituition.id
        if type_id == 3:
            validate_data["university"] = university.id
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validate_data, "id": certificate.id, "file": certificate.file}

class CertificateModelTwoSerializer(ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "house"]

class CertificateModelThreeCreateSerializer(ModelSerializer):
    date = serializers.DateField(allow_null=True)
    file = serializers.FileField(read_only=True)
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "house", "date", "file"]

    @atomic()
    def update(self, instance, validated_data):                              
        current_year = date.today().year
        certificates = Certificate.objects.filter(type_id=self.context['type_id'], date_issue__year=current_year)
        validated_data["number"] = get_number(current_year, certificates, instance, self.context['type_id'])
        validated_data["type_id"] = int(self.context['type_id'])
        new_validate_data = validated_data.copy()
        del new_validate_data["date"]
        certificate = super().update(instance, new_validate_data)
        model = AtestadoThird(DocumentData(validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.filter(pk=certificate.id).update(house=validated_data["main_person"].address)
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):
        current_year = date.today().year
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = int(self.context['type_id'])
        new_validate_data = validate_data.copy()
        del new_validate_data["date"]
        certificate = super().create(new_validate_data)
        model = AtestadoThird(DocumentData(validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.create(certificate_id=certificate.id, house=validate_data["main_person"].address)
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validate_data, "id": certificate.id, "file": certificate.file}

class CertificateModelThreeSerializer(ModelSerializer):
    date = serializers.DateField(read_only=True)
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "house", "date"]

class CertificateModelFifthCreateSerializer(ModelSerializer):
    instituition = serializers.IntegerField()
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "house", "instituition", "file"]

    def validate_institution(self, institution):
        if not institution:
            raise serializers.ValidationError({'institution': "Select instituition"})
        elif not Instituition.objects.filter(id=institution).exists():
            raise serializers.ValidationError({'institution': "This instituition is not valid"})
        return institution

    @atomic()
    def update(self, instance, validated_data):
        current_year = date.today().year
        certificates = Certificate.objects.filter(type_id=self.context['type_id'], date_issue__year=current_year)
        validated_data["number"] = get_number(current_year, certificates, instance, self.context['type_id'])
        validated_data["type_id"] = int(self.context['type_id'])
        validated_data["status"] = "P"
        new_validate_data = validated_data.copy()
        del new_validate_data["instituition"]
        certificate = super().update(instance, new_validate_data)
        instituition = Instituition.objects.filter(id=validated_data["instituition"]).first()
        model = AtestadoFifth(DocumentData(validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.filter(pk=certificate.id).update(house=validated_data["main_person"].address)
        validated_data["instituition"] = instituition.id
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):
        if int(self.context['type_id']) == 12:
            if CertificateSimplePerson.objects.filter(type_id=12).count() == 0:
                raise serializers.ValidationError({'persons': "No simple persons"})
            elif CertificateSinglePerson.objects.filter(type_id=12).count() == 0:
                raise serializers.ValidationError({'persons': "No single person"})
        current_year = date.today().year
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = int(self.context['type_id'])
        new_validate_data = validate_data.copy()
        del new_validate_data["instituition"]
        certificate = super().create(new_validate_data)
        instituition = Instituition.objects.filter(id=validate_data["instituition"]).first()
        model = AtestadoFifth(DocumentData(validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.create(certificate_id=certificate.id, house=validate_data["main_person"].address)
        validate_data["instituition"] = instituition.id
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validate_data, "id": certificate.id, "file": certificate.file}

class CertificateModelFifthSerializer(ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "house"]

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

class CertificateModelEnterroCreateSerializer(ModelSerializer):
    cemiterio = serializers.IntegerField()
    died_date = serializers.DateField()
    entero_date = serializers.DateField()
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "cemiterio", "died_date", "entero_date", "file"]

    def validate_cemiterio(self, cemiterio):
        if not cemiterio:
            raise serializers.ValidationError({'cemiterio': "Select cemiterio"})
        elif not Cemiterio.objects.filter(id=cemiterio).exists():
            raise serializers.ValidationError({'cemiterio': "This cemiterio is not valid"})
        return cemiterio

    @atomic()
    def update(self, instance, validated_data):
        current_year = date.today().year
        certificates = Certificate.objects.filter(type_id=self.context['type_id'], date_issue__year=current_year)
        validated_data["number"] = get_number(current_year, certificates, instance, self.context['type_id'])
        type_id = validated_data["type_id"] = int(self.context['type_id'])
        validated_data["status"] = "P"
        new_validate_data = validated_data.copy()
        del new_validate_data["cemiterio"]
        del new_validate_data["died_date"]
        del new_validate_data["entero_date"]
        certificate = super().update(instance, new_validate_data)
        cemiterio = Cemiterio.objects.filter(id=validated_data["cemiterio"]).first()
        startdate = date.today()
        covals = Coval.objects.filter(date_used__year__lt=(startdate.year - 1), closed=False, cemiterio=cemiterio).order_by("square", "date_used")
        if not covals:
            raise serializers.ValidationError({'coval': 'There is no space'})
        elif not CertificateSinglePerson.objects.filter(type_id=type_id).exists():
            raise serializers.ValidationError({'coval': 'You must add a single the died person details'})
        coval = covals.first()
        coval.closed = True
        coval.save()
        person = CertificateSinglePerson.objects.get(type_id=type_id)
        new_coval = {
            'number': f"{covals.filter(square=coval.square).count()+1}-{startdate.year} {coval.square}",
            'nick_number': f"{coval.nick_number}",
            'name': f"{person.name}",
            'date_used': f"{validated_data['entero_date']}",
            'date_of_deth': f"{validated_data['died_date']}",
            'gender': f"{person.gender}",
            'square': f"{coval.square}"
        }
        Coval.objects.create(**new_coval)
        model = AutoEnterro(DocumentData(validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))
        text, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=instance.id).update(text=text, status="P")
        CertificateData.objects.filter(pk=instance.id).update(house=validated_data["main_person"].address)
        validated_data["cemiterio"] = cemiterio.id
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):
        current_year = date.today().year
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        type_id = validate_data["type_id"] = int(self.context['type_id'])
        new_validate_data = validate_data.copy()
        del new_validate_data["cemiterio"]
        del new_validate_data["died_date"]
        del new_validate_data["entero_date"]
        certificate = super().create(new_validate_data)
        cemiterio = Cemiterio.objects.filter(id=validate_data["cemiterio"]).first()
        startdate = date.today()
        covals = Coval.objects.filter(date_used__year__lt=(startdate.year - 1), closed=False, cemiterio=cemiterio).order_by("square", "date_used")
        if not covals:
            raise serializers.ValidationError({'coval': 'There is no space'})
        elif not CertificateSinglePerson.objects.filter(type_id=type_id).exists():
            raise serializers.ValidationError({'coval': 'You must add a single the died person details'})
        coval = covals.first()
        coval.closed = True
        coval.save()
        person = CertificateSinglePerson.objects.get(type_id=type_id)
        new_coval = {
            'number': f"{covals.filter(square=coval.square).count()+1}-{startdate.year} {coval.square}",
            'nick_number': f"{coval.nick_number}",
            'name': f"{person.name}",
            'date_used': f"{validate_data['entero_date']}",
            'date_of_deth': f"{validate_data['died_date']}",
            'gender': f"{person.gender}",
            'square': f"{coval.square}"
        }
        Coval.objects.create(**new_coval)
        model = AutoEnterro(DocumentData(validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        text, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.create(certificate_id=certificate.id, house=validate_data["main_person"].address)
        validate_data["cemiterio"] = cemiterio.id
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validate_data, "id": certificate.id, "file": certificate.file}

class CertificateModelEnterroSerializer(ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "house"]

class CertificateModelCertCompraCovalCreateSerializer(ModelSerializer):
    coval = serializers.IntegerField()
    file = serializers.FileField(read_only=True)
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "coval", "file"]

    def validate_coval(self, coval):
        if not coval:
            raise serializers.ValidationError("Select coval")
        coval_obj = Coval.objects.filter(id=coval).first()
        if not coval_obj:
            raise serializers.ValidationError("This coval is not valid")
        if coval_obj.date_of_deth == None:
            raise serializers.ValidationError("Empty coval")
        if CovalSalles.objects.filter(coval__id=coval).exists():
            raise serializers.ValidationError("Coval is selled")
        return coval

    @atomic()
    def update(self, instance, validated_data):
        current_year = date.today().year
        certificates = Certificate.objects.filter(type_id=self.context['type_id'], date_issue__year=current_year)
        validated_data["number"] = get_number(current_year, certificates, instance, self.context['type_id'])
        type_id = int(self.context['type_id'])
        new_validate_data = validated_data.copy()
        del new_validate_data["coval"]
        certificate = super().update(instance, new_validate_data)
        coval = Coval.objects.get(id=validated_data["coval"])
        model = None
        if type_id == 24:
            coval.selled = True
            coval.save()
            CovalSalles.objects.create(coval_id=coval.id, person_id=validated_data["main_person"].id)
            model = CertCompraCoval(DocumentData(validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))
        elif type_id == 30:
            model = LicencaTransladacao(DocumentData(validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))
        text, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.filter(pk=certificate.id).update(house=validated_data["main_person"].address)
        validated_data["coval"] = coval.id
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):
        current_year = date.today().year
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        type_id = int(self.context['type_id'])
        new_validate_data = validate_data.copy()
        del new_validate_data["coval"]
        certificate = super().create(new_validate_data)
        coval = Coval.objects.get(id=validate_data["coval"])
        model = None
        if type_id == 24:
            coval.selled = True
            coval.save()
            CovalSalles.objects.create(coval_id=coval.id, person_id=validate_data["main_person"].id)
            model = CertCompraCoval(DocumentData(validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        elif type_id == 30:
            model = LicencaTransladacao(DocumentData(validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.create(certificate_id=certificate.id, house=validate_data["main_person"].address)
        validate_data["coval"] = coval.id
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validate_data, "id": certificate.id, "file": certificate.file}

class CertificateModelCertCompraCovalSerializer(ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person"]

class CertificateModelAutoModCovalCreateSerializer(ModelSerializer):
    coval = serializers.IntegerField()
    change = serializers.IntegerField()
    file = serializers.FileField(read_only=True)
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "coval", "change", "file"]

    def validate_coval(self, coval):
        if not coval:
            raise serializers.ValidationError({'coval': "Select coval"})
        if not Coval.objects.filter(id=coval).exists():
            raise serializers.ValidationError({'coval': "This coval is not valid"})
        return coval

    def validate_change(self, change):
        if not change:
            raise serializers.ValidationError({'change': "Select change"})
        if not Change.objects.filter(id=change).exists():
            raise serializers.ValidationError({'change': "This change is not valid"})
        return change

    @atomic()
    def update(self, instance, validated_data):                              
        current_year = date.today().year
        certificates = Certificate.objects.filter(type_id=self.context['type_id'], date_issue__year=current_year)
        validated_data["number"] = get_number(current_year, certificates, instance, self.context['type_id'])
        validated_data["type_id"] = int(self.context['type_id'])
        validated_data["status"] = "P"
        new_validate_data = validated_data.copy()
        del new_validate_data["coval"]
        del new_validate_data["change"]
        certificate = super().update(instance, new_validate_data)
        coval = Coval.objects.get(id=validated_data["coval"])
        change = Change.objects.get(id=validated_data["change"])
        model = AutoModCovalAndLicBarraca(DocumentData(validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.filter(pk=certificate.id).update(house=validated_data["main_person"].address)
        validated_data["coval"] = coval.id
        validated_data["change"] = change.id
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):
        current_year = date.today().year
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = int(self.context['type_id'])
        new_validate_data = validate_data.copy()
        del new_validate_data["coval"]
        del new_validate_data["change"]
        certificate = super().create(new_validate_data)
        coval = Coval.objects.get(id=validate_data["coval"])
        change = Change.objects.get(id=validate_data["change"])
        model = AutoModCovalAndLicBarraca(DocumentData(validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.create(certificate_id=certificate.id, house=validate_data["main_person"].address)
        validate_data["coval"] = coval.id
        validate_data["change"] = change.id
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validate_data, "id": certificate.id, "file": certificate.file}

class CertificateModelAutoModCovalSerializer(ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person"]

class CertificateModelLicBarracaCreateSerializer(ModelSerializer):
    object = serializers.CharField()
    street = serializers.IntegerField()
    file = serializers.FileField(read_only=True)
    range = serializers.CharField()
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "object", "street", "file", "range"]

    def validate_object(self, object):
        if not object:
            raise serializers.ValidationError({'object': "Type the object"})
        return object

    def validate_street(self, street):
        if not street:
            raise serializers.ValidationError({'street': "Select street"})
        if not Street.objects.filter(id=street).exists():
            raise serializers.ValidationError({'street': "This street is not valid"})
        return street

    @atomic()
    def update(self, instance, validated_data):                              
        current_year = date.today().year
        certificates = Certificate.objects.filter(type_id=self.context['type_id'], date_issue__year=current_year)
        validated_data["number"] = get_number(current_year, certificates, instance, self.context['type_id'])
        validated_data["type_id"] = int(self.context['type_id'])
        validated_data["status"] = "P"
        new_validate_data = validated_data.copy()
        del new_validate_data["object"]
        del new_validate_data["street"]
        del new_validate_data["range"]
        certificate = super().update(instance, new_validate_data)
        street = Street.objects.get(id=validated_data["street"])
        if validated_data["type_id"] == 27:
            validated_data["range"] = CertificateRange.objects.get(type=validated_data["range"])
        model = AutoModCovalAndLicBarraca(DocumentData(validated_data["main_person"], validated_data, certificate, validated_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.filter(pk=certificate.id).update(house=validated_data["main_person"].address)
        validated_data["street"] = street.id
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):
        current_year = date.today().year
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = int(self.context['type_id'])
        new_validate_data = validate_data.copy()
        del new_validate_data["object"]
        del new_validate_data["street"]
        del new_validate_data["range"]
        certificate = super().create(new_validate_data)
        street = Street.objects.get(id=validate_data["street"])
        if validate_data["type_id"] == 27:
            validate_data["range"] = CertificateRange.objects.get(type=validate_data["range"])
        model = AutoModCovalAndLicBarraca(DocumentData(validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.create(certificate_id=certificate.id, house=validate_data["main_person"].address)
        validate_data["street"] = street.id
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validate_data, "id": certificate.id, "file": certificate.file}

class CertificateModelLicBarracaSerializer(ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person"]

class CertificateModelAutoConstrucaoCreateSerializer(ModelSerializer):
    building_type = serializers.IntegerField()
    street = serializers.IntegerField()
    file = serializers.FileField(read_only=True)
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "building_type", "street", "file"]

    def validate_building_type(self, building_type):
        if not building_type:
            raise serializers.ValidationError({'building_type': "Select building_type"})
        if not BiuldingType.objects.filter(id=building_type).exists():
            raise serializers.ValidationError({'building_type': "This building_type is not valid"})
        return building_type

    def validate_street(self, street):
        if not street:
            raise serializers.ValidationError({'street': "Select street"})
        if not Street.objects.filter(id=street).exists():
            raise serializers.ValidationError({'street': "This street is not valid"})
        return street

    @atomic()
    def update(self, instance, validated_data):                              
        current_year = date.today().year
        certificates = Certificate.objects.filter(type_id=self.context['type_id'], date_issue__year=current_year)
        validated_data["number"] = get_number(current_year, certificates, instance, self.context['type_id'])
        validated_data["type_id"] = int(self.context['type_id'])
        validated_data["status"] = "P"
        new_validate_data = validated_data.copy()
        del new_validate_data["building_type"]
        del new_validate_data["street"]
        certificate = super().update(instance, new_validate_data)
        building_type = BiuldingType.objects.get(id=validated_data["building_type"])
        street = Street.objects.get(id=validated_data["street"])
        model = AutoConstrucao(DocumentData(validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=instance.id).update(text=text, status="P")
        CertificateData.objects.filter(pk=instance.id).update(house=validated_data["main_person"].address)
        validated_data["building_type"] = building_type.id
        validated_data["street"] = street.id
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):
        current_year = date.today().year
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = int(self.context['type_id'])
        new_validate_data = validate_data.copy()
        del new_validate_data["building_type"]
        del new_validate_data["street"]
        certificate = super().create(new_validate_data)
        building_type = BiuldingType.objects.get(id=validate_data["building_type"])
        street = Street.objects.get(id=validate_data["street"])
        model = AutoConstrucao(DocumentData(validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.create(certificate_id=certificate.id, house=validate_data["main_person"].address)
        validate_data["building_type"] = building_type.id
        validate_data["street"] = street.id
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validate_data, "id": certificate.id, "file": certificate.file}

class CertificateModelAutoConstrucaoSerializer(ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "house"]

class CertificateModelSeventhCreateSerializer(ModelSerializer):
    years = serializers.IntegerField()
    country = serializers.IntegerField(allow_null=True)
    file = serializers.FileField(read_only=True)
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "house", "years", "country", "file"]

    @atomic()
    def update(self, instance, validated_data):                              
        current_year = date.today().year
        certificates = Certificate.objects.filter(type_id=self.context['type_id'], date_issue__year=current_year)
        validated_data["number"] = get_number(current_year, certificates, instance, self.context['type_id'])
        validated_data["type_id"] = int(self.context['type_id'])
        validated_data["status"] = "P"
        new_validate_data = validated_data.copy()
        del new_validate_data["years"]
        del new_validate_data["country"]
        certificate = super().update(instance, new_validate_data)
        country = Country.objects.filter(id=validated_data["country"]).first()
        model = AtestadoSeventh(DocumentData(validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=instance.id).update(text=text, status="P")
        CertificateData.objects.filter(pk=instance.id).update(house=validated_data["main_person"].address)
        validated_data["country"] = country.id if country else None
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):
        current_year = date.today().year
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = int(self.context['type_id'])
        new_validate_data = validate_data.copy()
        del new_validate_data["years"]
        del new_validate_data["country"]
        certificate = super().create(new_validate_data)
        country = Country.objects.filter(id=validate_data["country"]).first()
        model = AtestadoSeventh(DocumentData(validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.create(certificate_id=certificate.id, house=validate_data["main_person"].address)
        validate_data["country"] = country.id if country else None
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validate_data, "id": certificate.id, "file": certificate.file}

class CertificateModelSeventhSerializer(ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "house"]

class CertificateModelLicencaBuffetCreateSerializer(ModelSerializer):
    infra = serializers.CharField()
    street = serializers.IntegerField()
    metros = serializers.IntegerField(allow_null=True)
    file = serializers.FileField(read_only=True)
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person", "infra", "street", "metros", "file"]

    @atomic()
    def update(self, instance, validated_data):                              
        current_year = date.today().year
        certificates = Certificate.objects.filter(type_id=self.context['type_id'], date_issue__year=current_year)
        validated_data["number"] = get_number(current_year, certificates, instance, self.context['type_id'])
        type_id = validated_data["type_id"] = int(self.context['type_id'])
        validated_data["status"] = "P"
        new_validate_data = validated_data.copy()
        del new_validate_data["infra"]
        del new_validate_data["street"]
        del new_validate_data["metros"]
        certificate = super().update(instance, new_validate_data)
        street = Street.objects.filter(id=validated_data["street"]).first()
        validated_data["last_date"] = CertificateDate.objects.filter(type_id=type_id).order_by('-date').first().date
        validated_data["dates"] = CertificateDate.objects.filter(type_id=type_id).order_by('-date')
        model = LicencaBufett(DocumentData(validated_data["main_person"], validated_data, certificate, validated_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=instance.id).update(text=text, status="P")
        CertificateData.objects.filter(pk=instance.id).update(house=validated_data["main_person"].address)
        validated_data["street"] = street.id if street else None
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):
        current_year = date.today().year
        type_id = int(self.context['type_id'])
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = int(type_id)
        new_validate_data = validate_data.copy()
        del new_validate_data["infra"]
        del new_validate_data["street"]
        del new_validate_data["metros"]
        certificate = super().create(new_validate_data)
        street = Street.objects.filter(id=validate_data["street"]).first()
        validate_data["last_date"] = CertificateDate.objects.filter(type_id=type_id).order_by('-date').first().date
        validate_data["dates"] = CertificateDate.objects.filter(type_id=type_id).order_by('-date')
        model = LicencaBufett(DocumentData(validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        text, _, _ = StringHelper.renderText(model)
        Certificate.objects.filter(pk=certificate.id).update(text=text, status="P")
        CertificateData.objects.create(certificate_id=certificate.id, house=validate_data["main_person"].address)
        validate_data["street"] = street.id if street else None
        certificate = Certificate.objects.get(pk=certificate.id)
        return {**validate_data, "id": certificate.id, "file": certificate.file}

class CertificateModelLicencaBuffetSerializer(ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "main_person", "secondary_person"]

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
        CertificateSinglePerson.objects.filter(type_id=self.context['type_id']).delete()
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