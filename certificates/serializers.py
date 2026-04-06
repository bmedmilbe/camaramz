from pprint import pprint
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
from datetime import date, timedelta
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from templated_mail.mail import BaseEmailMessage
from django.db.transaction import atomic
import os
from django.core.mail import BadHeaderError
from django.apps import apps
from django.core.validators import MinValueValidator
from django.db.transaction import atomic
from decimal import Decimal
from django.conf import settings
from . import helpers
import requests
import json
from .classes.document_data import DocumentData
from .classes.document_form import DocumentForm

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
    Messages,
    Parent,
    Person,

    Customer,
    PersonBirthAddress,
    Street,
    Town,
    University,

)
from django.db.models import Sum
from django.db.transaction import atomic


class CustomerSerializer(ModelSerializer):
    first_name = serializers.SerializerMethodField(
        method_name="get_first_name")
    last_name = serializers.SerializerMethodField(method_name="get_last_name")
    back_staff = serializers.SerializerMethodField(method_name="get_back_staff")

    class Meta:
        model = Customer
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "back_staff",
            "level",

        ]

    def get_first_name(self, customer: Customer):
        return customer.user.first_name
    
    def get_back_staff(self, customer: Customer):
        return customer.backstaff

    def get_last_name(self, customer: Customer):
        return customer.user.last_name


class CountryCreateSerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = [
            "id",
            "name",
            "code",
        ]

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
        fields = [
            "id",
            "name",
            "code",
        ]

    


class CountyCreateSerializer(ModelSerializer):

    class Meta:
        model = County
        fields = [
            "id",
            "name",
            "country",
        ]

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
        fields = [
            "id",
            "name",
            "slug",
            "country",
        ]


class UniversityCreateSerializer(ModelSerializer):

    class Meta:
        model = University
        fields = [
            "id",
            "name",

        ]
    def create(self, validate_data):
        name = validate_data.get('name')
        object_list = University.objects.filter(name=name)
        if object_list:
            return object_list.first()
            
        return super().create(validate_data)
class UniversitySerializer(ModelSerializer):

    class Meta:
        model = University
        fields = [
            "id",
            "name",

        ]


class BiuldingTypeSerializer(ModelSerializer):

    class Meta:
        model = BiuldingType
        fields = [
            "id",
            "name",
            "prefix",

        ]


class TownCreateSerializer(ModelSerializer):

    class Meta:
        model = Town
        fields = [
            "id",
            "name",
            "county",
           
        ]

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
        fields = [
            "id",
            "name",
            "size",
        ]

class IfenUpdateSerializer(ModelSerializer):

    class Meta:
        model = Ifen
        fields = [
            "id",
            "size",
        ]
    
  

class TownSerializer(ModelSerializer):
    county = CountySerializer()
    country = serializers.SerializerMethodField(method_name="get_country")

    class Meta:
        model = Town
        fields = [
            "id",
            "name",
            "slug",
            "county",
            "country",
        ]

    def get_country(self, town):
        return f"{town.county.country.name}"


class StreetCreateSerializer(ModelSerializer):
    

    class Meta:
        model = Street
        fields = [
            "id",
            "name",
            "town",
        ]

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
        fields = [
            "id",
            "name",
            "town",
           
        ]

    # def get_town(self, street):
    #     return f"{street.town.name if street.town != None else '' }"

    # def get_county(self, street):
    #     return f"{street.town.county.name if street.town != None else ''}"

    # def get_country(self, street):
    #     return f"{street.town.county.country.name if street.town != None else ''}"


class HouseSerializer(ModelSerializer):
    street = StreetSerializer()

    class Meta:
        model = House
        fields = [
            "id",
            "house_number",
            "street",
        ]


class HouseCreateSerializer(ModelSerializer):
    house_number = serializers.CharField(allow_blank=True, required=False)
    class Meta:
        model = House
        fields = [
            "id",
            "house_number",
            "street",
        ]

    def create(self, validate_data):

        house_number = validate_data.get('house_number')
        
        house = House.objects.filter(
            house_number=house_number,
            street_id=validate_data['street']
        )

        if not house:
            validate_data["house_number"] = house_number if (house_number != -1 or not house_number)  else None
            return super().create(validate_data)
        return house.first()


class PersonBirthAddressSerializer(ModelSerializer):
    birth_street = StreetSerializer()
    birth_town = TownSerializer()
    birth_county = CountySerializer()
    birth_country = CountrySerializer()

    class Meta:
        model = PersonBirthAddress
        fields = [
            "id",
            "birth_street",
            "birth_town",
            "birth_county",
            "birth_country",
        ]
def remove_duplicates_by_number(list_of_dicts):
    """Removes dictionaries where the 'age' value is duplicated."""

    items_counts = {}
    dicts_to_remove = []

    # Count age occurrences
    for d in list_of_dicts:
        number = d.get("number")  # Use .get() to handle missing 'age' key
        if number is not None:
            items_counts[number] = items_counts.get(number, 0) + 1

    # Identify dictionaries with duplicated ages
    for d in list_of_dicts:
        number = d.get("number")
        if number is not None and items_counts[number] > 1:
            dicts_to_remove.append(d)

    # Create a new list without the duplicates
    new_list = [d for d in list_of_dicts if d not in dicts_to_remove]

    return new_list
def remove_duplicates_keep_one(list_of_dicts, key_to_check):
    """Removes duplicate dictionaries based on a given key, keeping only the first occurrence."""

    seen_values = set()
    new_list = []

    for d in list_of_dicts:
        value = d.get(key_to_check)
        if value is not None:
            if value not in seen_values:
                seen_values.add(value)
                new_list.append(d)
        else:
            new_list.append(d) # Keep dictionaries without the key

    return new_list
def get_number(current_year, certificates: Certificate, instance: Certificate,type_id):
    
    
    last = certificates.last()

    if instance.type.certificate_type.id == int(last.type.certificate_type.id):
        return instance.number
    # pprint(instance.type.id)
    # pprint(type_id)
    # pprint(last)
    last_obj = None
    
    if last != None:
        # items = Certificate.objects.filter(type__certificate_type__id = last.type.certificate_type.id, date_issue__year=current_year)
        items = Certificate.objects.filter(type__certificate_type__id = last.type.certificate_type.id, date_issue__year=current_year, number__endswith=current_year)

        if items.exists():
            items = [item for item in items.values()]
            last_obj = sorted(items, key=lambda item:int(item['number'].replace("-","") ), reverse=True)[0]
    
    if last_obj != None:
        
        return f"{int(last_obj['number'].split('-')[0]) + 1}-{current_year}"
        
    return f"{1}-{current_year}"

def set_number(current_year, type_id):
  
    last = CertificateTitle.objects.get(id=type_id)
    

    # last = Certificate.objects.filter(type__certificate_type__id = last.certificate_type.id, date_issue__year=current_year).last()
    last_obj = None
    
    if last != None:
        items = Certificate.objects.filter(type__certificate_type__id = last.certificate_type.id, date_issue__year=current_year, number__endswith=current_year)
        if items.exists():
            items = [item for item in items.values()]
            last_obj = sorted(items, key=lambda item:int(item['number'].replace("-","") ), reverse=True)[0]
    
            # pprint(last_obj)

    if last_obj != None:
        
        return f"{int(last_obj['number'].split('-')[0]) + 1}-{current_year}"
        
    return f"{1}-{current_year}"


# class PersonBirthAddressCreateSerializer(ModelSerializer):
#     birth_street = serializers.CharField( required=False)
#     birth_town = serializers.CharField( required=False)
#     birth_county = serializers.CharField( required=False)
#     birth_country = serializers.CharField()
#     # house_number = serializers.CharField(allow_blank=True, required=False)
#     class Meta:
#         model = PersonBirthAddress
#         fields = [
#             "id",
#             "birth_street",
#             "birth_town",
#             "birth_county",
#             "birth_country",
#         ]

#     def create(self, validate_data):
#         # pprint(validate_data)
#         street = Street.objects.filter(
#             id=validate_data['birth_street']).first()
#         town = Town.objects.filter(id=validate_data['birth_town']).first()
#         county = County.objects.filter(
#             id=validate_data['birth_county']).first()
#         # print(street)

#         del validate_data['birth_street']
#         del validate_data['birth_town']
#         del validate_data['birth_county']

#         validate_data['birth_street'] = None if street == None else street.id
#         validate_data['birth_town'] = None if town == None else town.id
#         validate_data['birth_county'] = None if county == None else county.id

#         # print(validate_data)

#         address = PersonBirthAddress.objects.filter(
#             birth_street=validate_data['birth_street'],
#             birth_town=validate_data['birth_town'],
#             birth_county=validate_data['birth_county'],
#             birth_country=validate_data['birth_country'],
#         )

#         if not address:
#             return super().create(validate_data)
#         return address.first()
    

class PersonBirthAddressCreateSerializer(ModelSerializer):
    
    birth_street = serializers.PrimaryKeyRelatedField(
        queryset=Street.objects.all(), 
        required=False, 
        allow_null=True
    )
    birth_town = serializers.PrimaryKeyRelatedField(
        queryset=Town.objects.all(), 
        required=False, 
        allow_null=True
    )
    birth_county = serializers.PrimaryKeyRelatedField(
        queryset=County.objects.all(), 
        required=False, 
        allow_null=True
    )
    
    birth_country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), 
        required=True 
    ) 

    class Meta:
        model = PersonBirthAddress
        fields = [
            "id",
            "birth_street",
            "birth_town",
            "birth_county",
            "birth_country",
        ]

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
            "id",
            "name",
            "surname",
            "birth_date",
            # "birth_street",
            # "birth_town",
            # "birth_county",
            # "birth_country",
            "birth_address",
            "id_type",
            "id_number",
            "id_issue_local",
            "id_issue_country",
            "nationality",
            "id_issue_date",
            "id_expire_date",
            "father_name",
            "mother_name",
            "address",
            "status",
            "gender",


        ]

    def create(self, validate_data):

        person = Person.objects.filter(
            # nationality=validate_data['nationality'],
            id_type=validate_data['id_type'],
            id_number=validate_data['id_number']
        )


        if not validate_data['father_name'] and not validate_data['mother_name']:
            raise serializers.ValidationError(
                {"person": "The person must to have a father or mother"})

        if not person:
            return super().create(validate_data)
        raise serializers.ValidationError(
            {"person": "There is a person with same ID already registered"})

    def update(self, instance, validate_data):

        # pprint(self.context)
        person = Person.objects.filter(

            id=self.context['id']
        )

        if not validate_data['father_name'] and not validate_data['mother_name']:
            raise serializers.ValidationError(
                {"person": "The person must to have a father or mother"})

        if person.first().id == instance.id:
            return super().update(instance, validate_data)
        raise serializers.ValidationError(
            {"person": "There is a person with same ID already registered"})


class IDTypeSerializer(ModelSerializer):

    class Meta:
        model = IDType
        fields = [
            "id",
            "name",
        ]


class InstituitionCreateSerializer(ModelSerializer):

    class Meta:
        model = Instituition
        fields = [
            "id",
            "name",
        ]
    def create(self, validate_data):
        name = validate_data.get('name')
        object_list = Instituition.objects.filter(name=name)
        if object_list:
            return object_list.first()
            
        return super().create(validate_data)
class InstituitionSerializer(ModelSerializer):

    class Meta:
        model = Instituition
        fields = [
            "id",
            "name",
        ]

    


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
            "id",
            "name",
            "surname",
            "birth_date",
            "birth_address",
            "id_type",
            "id_number",
            "id_issue_local",
            "id_issue_country",
            "nationality",
            "id_issue_date",
            "id_expire_date",
            "father_name",
            "mother_name",
            "address",
            "status",
            "gender",
        ]


class CertificateModelOneCreateSerializer(ModelSerializer):
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",
            "secondary_person",
            "house",
            "file",

        ]

    @atomic()
    def update(self, instance, validated_data):
        # pprint("Update")

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validated_data = dict()
        validated_data["number"] = get_number(current_year, certificates, instance,self.context['type_id'])
        validated_data["type_id"] = int(self.context['type_id'])
        text_helper = StringHelper()
        # pprint(validated_data)
        certificate = instance=super().update(instance, validated_data)

        model = AtestadoOne(DocumentData(
            validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))

        text, file_name, status = StringHelper.renderText(model)

        validated_data["text"] = text
        validated_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        # pprint(validated_data["file_name"])
        # Certificate.objects.update(certificate,text=validated_data["text"])
        Certificate.objects.filter(pk=certificate.id).update(
            text=validated_data["text"], status="P")

        CertificateData.objects.filter(pk=certificate.id).update(
            house=validated_data["main_person"].address)

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):

        # pprint(validate_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validate_data = dict()
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = int(self.context['type_id'])
        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validate_data.copy()

        certificate = super().create(new_validate_data)

        model = AtestadoOne(DocumentData(
            validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        # pprint(certificate.file)
        text, file_name, status = StringHelper.renderText(model)
        # pprint(text)
        validate_data["text"] = text
        # validate_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        # pprint(validate_data["file_name"])
        # Certificate.objects.update(certificate,text=validate_data["text"])
        Certificate.objects.filter(pk=certificate.id).update(
            text=validate_data["text"], status="P")

        CertificateData.objects.create(
            certificate_id=certificate.id, house=validate_data["main_person"].address)

        certificate = Certificate.objects.get(pk=certificate.id)
        # pprint(file_name)

        return {**validate_data, "id": certificate.id, "file": certificate.file}


class CertificateModelOneSerializer(ModelSerializer):

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",  # Get the address from person object, update it every time you create new cv
            "secondary_person",
            "house_id",  # house that this person used in this especific certificare
            "file",
        ]


class CertificateModelTwoCreateSerializer(ModelSerializer):

    instituition = serializers.IntegerField()
    university = serializers.IntegerField(allow_null=True)
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",
            "secondary_person",
            "house",
            "instituition",
            "university",
            "file"
        ]

    def validate_institution(self, institution):
        if not institution:
            raise serializers.ValidationError(
                {'institution': "Select instituition"})
        elif not Instituition.objects.filter(id=institution).exists():
            raise serializers.ValidationError(
                {'institution': "This instituition is not valid"})
        return institution

    def validate_university(self, university):
        if university:
            if not University.objects.filter(id=university).exists():
                raise serializers.ValidationError(
                    {'university': "This university is not valid"})

        return university

    @atomic()
    def update(self, instance, validated_data):
        # pprint(validated_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validated_data = dict()
        validated_data["number"] = get_number(current_year, certificates, instance,self.context['type_id'])
        validated_data["type_id"] = type_id = int(self.context['type_id'])
        validated_data["status"] = "P"
        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validated_data.copy()

        del new_validate_data["instituition"]
        del new_validate_data["university"]

        pprint(validated_data)
        certificate = super().update(instance, new_validate_data)

        validated_data["instituition"] = instituition = Instituition.objects.filter(
            id=validated_data["instituition"]).first()
        if type_id == 3:
            validated_data["university"] = university = University.objects.filter(
                id=validated_data["university"]).first()

        model = AtestadoSecond(DocumentData(
            validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))

        text, file_name, status = StringHelper.renderText(model)

        validated_data["text"] = text
        validated_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        pprint(validated_data["file_name"])
        # Certificate.objects.update(certificate,text=validated_data["text"])
        Certificate.objects.filter(pk=certificate.id).update(
            text=validated_data["text"], status="P")

        CertificateData.objects.filter(pk=certificate.id).update(
            house=validated_data["main_person"].address)

        validated_data["instituition"] = instituition.id
        if type_id == 3:
            validated_data["university"] = university.id

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):

        # pprint(validate_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validate_data = dict()
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        type_id = validate_data["type_id"] = int(self.context['type_id'])

        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validate_data.copy()

        del new_validate_data["instituition"]
        del new_validate_data["university"]

        certificate = super().create(new_validate_data)
        # pprint(validate_data)
        # pprint(validate_data["instituition"])
        # pprint(certificate.id)
        validate_data["instituition"] = instituition = Instituition.objects.filter(
            id=validate_data["instituition"]).first()
        if type_id == 3:
            validate_data["university"] = university = University.objects.filter(
                id=validate_data["university"]).first()

        model = AtestadoSecond(DocumentData(
            validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        # pprint( StringHelper.renderText(model))
        # pprint(certificate.file)
        text, file_name, status = StringHelper.renderText(model)

        validate_data["text"] = text
        # validate_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        # pprint(validate_data["file_name"])

        Certificate.objects.filter(pk=certificate.id).update(
            text=validate_data["text"], status="P")

        CertificateData.objects.create(
            certificate_id=certificate.id, house=validate_data["main_person"].address)
        validate_data["instituition"] = instituition.id
        if type_id == 3:
            validate_data["university"] = university.id

        certificate = Certificate.objects.get(pk=certificate.id)
        # pprint(file_name)

        return {**validate_data, "id": certificate.id, "file": certificate.file}


class CertificateModelTwoSerializer(ModelSerializer):
    # instituition = serializers.IntegerField()
    # university = serializers.IntegerField()

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",  # Get the address from person object, update it every time you create new cv
            "secondary_person",
            "house",  # house that this person used in this especific certificare
            # "instituition",
            # "university",
        ]


class CertificateModelThreeCreateSerializer(ModelSerializer):

    date = serializers.DateField(allow_null=True)
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",
            "secondary_person",
            "house",
            "date",
            "file"
        ]

    @atomic()
    def update(self, instance, validated_data):
        # pprint(validated_data)

        # set the number and type,
        # set and save the text in text dev  mode
        pprint("Update")

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validated_data = dict()
        validated_data["number"] = get_number(current_year, certificates, instance,self.context['type_id'])
        validated_data["type_id"] = int(self.context['type_id'])
        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validated_data.copy()

        del new_validate_data["date"]

        certificate = super().update(instance, new_validate_data)

        model = AtestadoThird(DocumentData(
            validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))

        text, file_name, status = StringHelper.renderText(model)

        validated_data["text"] = text
        validated_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        # pprint(validated_data["file_name"])
        # Certificate.objects.update(certificate,text=validated_data["text"])
        Certificate.objects.filter(pk=certificate.id).update(
            text=validated_data["text"], status="P")

        CertificateData.objects.filter(pk=certificate.id).update(
            house=validated_data["main_person"].address)

        certificate = Certificate.objects.get(pk=certificate.id)

        # return {"id": certificate.id, "file": certificate.file.url, **validated_data}
        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):

        # pprint(validate_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validate_data = dict()
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = int(self.context['type_id'])

        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validate_data.copy()

        del new_validate_data["date"]

        certificate = super().create(new_validate_data)
        # pprint(validate_data)
        # pprint(validate_data["instituition"])

        model = AtestadoThird(DocumentData(
            validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        # pprint( StringHelper.renderText(model))
        text, file_name, status = StringHelper.renderText(model)

        validate_data["text"] = text
        validate_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        # pprint(validate_data["file_name"])

        Certificate.objects.filter(pk=certificate.id).update(
            text=validate_data["text"], status="P")

        CertificateData.objects.create(
            certificate_id=certificate.id, house=validate_data["main_person"].address)

        certificate = Certificate.objects.get(pk=certificate.id)

        # print("file", certificate.file.url)
        return {**validate_data, "id": certificate.id, "file": certificate.file}


class CertificateModelThreeSerializer(ModelSerializer):
    date = serializers.DateField(read_only=True)

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",  # Get the address from person object, update it every time you create new cv
            "secondary_person",
            "house",  # house that this person used in this especific certificare
            "date",
        ]
# class CertificateModelFifthCreateSerializer(ModelSerializer):


#     class Meta:
#         model = Certificate
#         fields = [
#             "id",
#             "main_person",
#             "secondary_person",
#             "house",
#         ]

#     @atomic()
#     def create(self, validate_data):

#         # pprint(validate_data)

#         #set the number and type,
#         #set and save the text in text dev  mode

#         current_year = date.today().year
#         certificates = Certificate.objects.filter(type_id=self.context['type_id'],date_issue__year=current_year)
#         # validate_data = dict()
#         validate_data["number"] = set_number(current_year, self.context['type_id'])
#         validate_data["type_id"] = int(self.context['type_id'])

#         text_helper = StringHelper()
#         # pprint(validate_data)
#         new_validate_data = validate_data.copy()

#         del new_validate_data["date"]

#         certificate =  super().create(new_validate_data)
#         # pprint(validate_data)
#         # pprint(validate_data["instituition"])


#         model = AtestadoFifth(DocumentData(validate_data["main_person"],validate_data,certificate,validate_data["secondary_person"]))
#         # pprint( StringHelper.renderText(model))
#         text, file_name, status = StringHelper.renderText(model)

        # validate_data["text"] = text
        # validate_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        # pprint(validate_data["file_name"])

#         Certificate.objects.filter(pk=certificate.id).update(text=validate_data["text"])


#         CertificateData.objects.create(certificate_id=certificate.id,house=validate_data["main_person"].address)


#         CertificateSimplePerson.objects.filter(type_id=self.context['type_id']).delete() # removel all saved by current user and add next
#         # CertificateSimplePerson.objects.filter(type_id=self.context['type_id'], user_id=self.context['user_id']).delete() # removel all saved by current user and add next

#         return {"id":f"{certificate.id}", **validate_data}

# class CertificateModelFifthSerializer(ModelSerializer):


#     class Meta:
#         model = Certificate
#         fields = [
#             "id",
#             "main_person",  # Get the address from person object, update it every time you create new cv
#             "secondary_person",
#             "house", #house that this person used in this especific certificare

#         ]


class CertificateModelFifthCreateSerializer(ModelSerializer):

    instituition = serializers.IntegerField()
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",
            "secondary_person",
            "house",
            "instituition",
            "file",

        ]

    def validate_institution(self, institution):
        if not institution:
            raise serializers.ValidationError(
                {'institution': "Select instituition"})
        elif not Instituition.objects.filter(id=institution).exists():
            raise serializers.ValidationError(
                {'institution': "This instituition is not valid"})
        

        return institution

    @atomic()
    def update(self, instance, validated_data):
        # pprint(validated_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validated_data = dict()
        validated_data["number"] = get_number(current_year, certificates, instance,self.context['type_id'])
        validated_data["type_id"] = type_id = int(self.context['type_id'])
        validated_data["status"] = "P"
        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validated_data.copy()

        del new_validate_data["instituition"]

        pprint(validated_data)
        certificate = super().update(instance, new_validate_data)

        validated_data["instituition"] = instituition = Instituition.objects.filter(
            id=validated_data["instituition"]).first()

        model = AtestadoFifth(DocumentData(
            validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))

        text, file_name, status = StringHelper.renderText(model)

        validated_data["text"] = text
        validated_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        pprint(validated_data["file_name"])
        # Certificate.objects.update(certificate,text=validated_data["text"])
        Certificate.objects.filter(pk=certificate.id).update(
            text=validated_data["text"], status="P")

        CertificateData.objects.filter(pk=certificate.id).update(
            house=validated_data["main_person"].address)

        validated_data["instituition"] = instituition.id

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):

        # pprint(validate_data)

        # set the number and type,
        # set and save the text in text dev  mode

        if int(self.context['type_id']) == 12:
            
            if CertificateSimplePerson.objects.filter(type_id=12).count() == 0:
                raise serializers.ValidationError(
                {'persons': "No simple persons"})
            elif CertificateSinglePerson.objects.filter(type_id=12).count() == 0:
                raise serializers.ValidationError(
                {'persons': "No single person"})


        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validate_data = dict()
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = int(self.context['type_id'])

        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validate_data.copy()

        del new_validate_data["instituition"]

        certificate = super().create(new_validate_data)
        # pprint(validate_data)
        # pprint(validate_data["instituition"])
        validate_data["instituition"] = instituition = Instituition.objects.filter(
            id=validate_data["instituition"]).first()
        


        model = AtestadoFifth(DocumentData(
            validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        # pprint( StringHelper.renderText(model))
        text, file_name, status = StringHelper.renderText(model)

        validate_data["text"] = text
        validate_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        pprint(validate_data["file_name"])

        Certificate.objects.filter(pk=certificate.id).update(
            text=validate_data["text"], status="P")

        CertificateData.objects.create(
            certificate_id=certificate.id, house=validate_data["main_person"].address)
        validate_data["instituition"] = instituition.id

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validate_data, "id": certificate.id, "file": certificate.file}


class CertificateModelFifthSerializer(ModelSerializer):
    # instituition = serializers.IntegerField()

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",  # Get the address from person object, update it every time you create new cv
            "secondary_person",
            "house",  # house that this person used in this especific certificare
            # "instituition",
        ]


class CovalSerializer(ModelSerializer):
    # instituition = serializers.IntegerField()

    class Meta:
        model = Coval
        fields = [
            "id", "nick_number", "number", "name", "date_used", "closed", "selled"
        ]


class CemiterioSerializer(ModelSerializer):
    # instituition = serializers.IntegerField()

    class Meta:
        model = Cemiterio
        fields = [
            "id", "name", "county"
        ]


class ChangeSerializer(ModelSerializer):
    # instituition = serializers.IntegerField()

    class Meta:
        model = Change
        fields = [
            "id", "name",
        ]


class CertificateModelEnterroCreateSerializer(ModelSerializer):

    cemiterio = serializers.IntegerField()
    died_date = serializers.DateField()
    entero_date = serializers.DateField()
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",
            "secondary_person",
            # "house",
            "cemiterio",
            "died_date",
            "entero_date",
            "file"
        ]

    def validate_cemiterio(self, cemiterio):
        if not cemiterio:
            raise serializers.ValidationError(
                {'cemiterio': "Select cemiterio"})
        elif not Cemiterio.objects.filter(id=cemiterio).exists():
            raise serializers.ValidationError(
                {'cemiterio': "This cemiterio is not valid"})
        return cemiterio

    @atomic()
    def update(self, instance, validated_data):
        # pprint(validated_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validated_data = dict()
        validated_data["number"] = get_number(current_year, certificates, instance,self.context['type_id'])
        validated_data["type_id"] = type_id = int(self.context['type_id'])
        validated_data["status"] = "P"
        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validated_data.copy()

        del new_validate_data["cemiterio"]
        del new_validate_data["died_date"]
        del new_validate_data["entero_date"]

        certificate = super().update(instance, new_validate_data)

        validated_data["cemiterio"] = cemiterio = Cemiterio.objects.filter(
            id=validated_data["cemiterio"]).first()

        # 5 years ago
        startdate = date.today()
        enddate = startdate - timedelta(days=365)  # five years ago
        covals = Coval.objects.filter(date_used__year__lt=enddate.year, closed=False,
                                      cemiterio=validated_data["cemiterio"]).order_by("square", "date_used")

        # add user when have session
        if not covals:
            raise serializers.ValidationError({'coval': 'There is no space'})
        elif not CertificateSinglePerson.objects.filter(type_id=type_id).exists():
            raise serializers.ValidationError(
                {'coval': 'You must add a single the died person details'})

        if covals:
            current_year = startdate.year
            validated_data['last_coval'] = coval = covals.first()
            coval.closed = True
            coval.save()
            person = CertificateSinglePerson.objects.get(type_id=type_id)
            new_coval = dict()
            new_coval['number'] = f"{covals.filter(square=coval.square).count()+1}-{current_year} {coval.square}"
            new_coval['nick_number'] = f"{coval.nick_number}"
            new_coval['name'] = f"{person.name}"
            new_coval['date_used'] = f"{validated_data['entero_date']}"
            new_coval['date_of_deth'] = f"{validated_data['died_date']}"
            new_coval['gender'] = f"{person.gender}"
            new_coval['square'] = f"{coval.square}"
            validated_data['coval'] = Coval.objects.create(**new_coval)

        model = AutoEnterro(DocumentData(
            validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))
        # pprint( StringHelper.renderText(model))
        text, file_name, status = StringHelper.renderText(model)

        validated_data["text"] = text
        validated_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        pprint(validated_data["file_name"])

        Certificate.objects.filter(pk=instance.id).update(
            text=validated_data["text"], status="P")

        CertificateData.objects.filter(pk=instance.id).update(
            house=validated_data["main_person"].address)

        validated_data["cemiterio"] = cemiterio.id
        del validated_data['coval']
        del validated_data['last_coval']

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):

        # pprint(validate_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validate_data = dict()
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = type_id = int(self.context['type_id'])

        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validate_data.copy()

        del new_validate_data["cemiterio"]
        del new_validate_data["died_date"]
        del new_validate_data["entero_date"]

        certificate = super().create(new_validate_data)
        # pprint(validate_data)
        # pprint(validate_data["instituition"])
        validate_data["cemiterio"] = cemiterio = Cemiterio.objects.filter(
            id=validate_data["cemiterio"]).first()

        # 5 years ago
        startdate = date.today()
        enddate = startdate - timedelta(days=365)  # five years ago
        covals = Coval.objects.filter(date_used__year__lt=enddate.year, closed=False,
                                      cemiterio=validate_data["cemiterio"]).order_by("square", "date_used")

        # add user when have session
        if not covals:
            raise serializers.ValidationError({'coval': 'There is no space'})
        elif not CertificateSinglePerson.objects.filter(type_id=type_id).exists():
            raise serializers.ValidationError(
                {'coval': 'You must add a single the died person details'})

        if covals:
            current_year = startdate.year
            validate_data['last_coval'] = coval = covals.first()
            coval.closed = True
            coval.save()
            person = CertificateSinglePerson.objects.get(type_id=type_id)
            new_coval = dict()
            new_coval['number'] = f"{covals.filter(square=coval.square).count()+1}-{current_year} {coval.square}"
            new_coval['nick_number'] = f"{coval.nick_number}"
            new_coval['name'] = f"{person.name}"
            new_coval['date_used'] = f"{validate_data['entero_date']}"
            new_coval['date_of_deth'] = f"{validate_data['died_date']}"
            new_coval['gender'] = f"{person.gender}"
            new_coval['square'] = f"{coval.square}"
            validate_data['coval'] = Coval.objects.create(**new_coval)

        model = AutoEnterro(DocumentData(
            validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        # pprint( StringHelper.renderText(model))
        text, file_name, status = StringHelper.renderText(model)

        validate_data["text"] = text
        validate_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        pprint(validate_data["file_name"])

        Certificate.objects.filter(pk=certificate.id).update(
            text=validate_data["text"], status="P")

        CertificateData.objects.create(
            certificate_id=certificate.id, house=validate_data["main_person"].address)
        validate_data["cemiterio"] = cemiterio.id
        del validate_data['coval']
        del validate_data['last_coval']

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validate_data, "id": certificate.id, "file": certificate.file}


class CertificateModelEnterroSerializer(ModelSerializer):
    # instituition = serializers.IntegerField()

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",  # Get the address from person object, update it every time you create new cv
            "secondary_person",
            "house",  # house that this person used in this especific certificare
            # "instituition",
        ]


class CertificateModelCertCompraCovalCreateSerializer(ModelSerializer):

    coval = serializers.IntegerField()
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",
            "secondary_person",
            "coval",
            "file"
        ]

    def validate_coval(self, coval):
        if not coval:
            raise serializers.ValidationError("Select coval")
        elif not Coval.objects.filter(id=coval).exists():
            raise serializers.ValidationError(
                "This coval is not valid")

        elif Coval.objects.filter(id=coval).first().date_of_deth == None:
            raise serializers.ValidationError(
                "Empty coval")
        elif CovalSalles.objects.filter(coval__id=coval).exists():
            raise serializers.ValidationError(
                "Coval is selled")
        return coval

    @atomic()
    def update(self, instance, validated_data):
        # pprint(validated_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validated_data = dict()
        validated_data["number"] = get_number(current_year, certificates, instance,self.context['type_id'])
        validated_data["type_id"] = type_id = int(self.context['type_id'])
        validated_data["status"] = "P"
        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validated_data.copy()

        del new_validate_data["coval"]

        certificate = super().update(instance, new_validate_data)

        validated_data["coval"] = coval = Coval.objects.filter(
            id=validated_data["coval"]).first()
        model = None
        pprint(type_id)
        if type_id == 24:
            coval.selled = True
            coval.save()

            CovalSalles.objects.create(
                coval_id=coval.id, person_id=validated_data["main_person"].id)
            model = CertCompraCoval(DocumentData(
                validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))

        if type_id == 30:
            model = LicencaTransladacao(DocumentData(
                validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))

        # pprint( StringHelper.renderText(model))
        text, file_name, status = StringHelper.renderText(model)

        validated_data["text"] = text
        validated_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        pprint(validated_data["file_name"])

        Certificate.objects.filter(pk=certificate.id).update(
            text=validated_data["text"], status="P")

        CertificateData.objects.filter(pk=certificate.id).update(
            house=validated_data["main_person"].address)

        validated_data["coval"] = coval.id

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):

        # pprint(validate_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validate_data = dict()
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = type_id = int(self.context['type_id'])

        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validate_data.copy()

        del new_validate_data["coval"]

        certificate = super().create(new_validate_data)
        # pprint(validate_data)
        # pprint(validate_data["instituition"])
        validate_data["coval"] = coval = Coval.objects.filter(
            id=validate_data["coval"]).first()
        model = None
        pprint(type_id)
        if type_id == 24:
            coval.selled = True
            coval.save()

            CovalSalles.objects.create(
                coval_id=coval.id, person_id=validate_data["main_person"].id)
            model = CertCompraCoval(DocumentData(
                validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))

        if type_id == 30:
            model = LicencaTransladacao(DocumentData(
                validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))

        # pprint( StringHelper.renderText(model))
        text, file_name, status = StringHelper.renderText(model)

        validate_data["text"] = text
        validate_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        pprint(validate_data["file_name"])

        Certificate.objects.filter(pk=certificate.id).update(
            text=validate_data["text"], status="P")

        CertificateData.objects.create(
            certificate_id=certificate.id, house=validate_data["main_person"].address)
        validate_data["coval"] = coval.id

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validate_data, "id": certificate.id, "file": certificate.file}


class CertificateModelCertCompraCovalSerializer(ModelSerializer):
    # instituition = serializers.IntegerField()

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",  # Get the address from person object, update it every time you create new cv
            "secondary_person",
            # "instituition",
        ]


class CertificateModelAutoModCovalCreateSerializer(ModelSerializer):

    coval = serializers.IntegerField()
    change = serializers.IntegerField()
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",
            "secondary_person",
            "coval",
            "change",
            "file"
        ]

    def validate_coval(self, coval):
        if not coval:
            raise serializers.ValidationError({'coval': "Select coval"})
        elif not Coval.objects.filter(id=coval).exists():
            raise serializers.ValidationError(
                {'coval': "This coval is not valid"})
        return coval

    def validate_change(self, change):
        if not change:
            raise serializers.ValidationError({'change': "Select change"})
        elif not Change.objects.filter(id=change).exists():
            raise serializers.ValidationError(
                {'change': "This change is not valid"})
        return change

    @atomic()
    def update(self, instance, validated_data):
        # pprint(validated_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validated_data = dict()
        validated_data["number"] = get_number(current_year, certificates, instance,self.context['type_id'])
        validated_data["type_id"] = type_id = int(self.context['type_id'])
        validated_data["status"] = "P"
        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validated_data.copy()

        del new_validate_data["coval"]
        del new_validate_data["change"]

        pprint(validated_data)
        certificate = super().update(instance, new_validate_data)

        validated_data["coval"] = coval = Coval.objects.filter(
            id=validated_data["coval"]).first()
        validated_data["change"] = change = Change.objects.filter(
            id=validated_data["change"]).first()

        model = AutoModCovalAndLicBarraca(DocumentData(
            validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))
        # pprint( StringHelper.renderText(model))
        text, file_name, status = StringHelper.renderText(model)

        validated_data["text"] = text
        validated_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        pprint(validated_data["file_name"])

        # Certificate.objects.update(certificate,text=validated_data["text"])
        Certificate.objects.filter(pk=certificate.id).update(
            text=validated_data["text"], status="P")

        CertificateData.objects.filter(pk=certificate.id).update(
            house=validated_data["main_person"].address)

        validated_data["coval"] = coval.id
        validated_data["change"] = change.id

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):

        # pprint(validate_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validate_data = dict()
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = type_id = int(self.context['type_id'])

        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validate_data.copy()

        del new_validate_data["coval"]
        del new_validate_data["change"]

        certificate = super().create(new_validate_data)
        # pprint(validate_data)
        # pprint(validate_data["instituition"])

        validate_data["coval"] = coval = Coval.objects.filter(
            id=validate_data["coval"]).first()
        validate_data["change"] = change = Change.objects.filter(
            id=validate_data["change"]).first()

        model = AutoModCovalAndLicBarraca(DocumentData(
            validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        # pprint( StringHelper.renderText(model))
        text, file_name, status = StringHelper.renderText(model)

        validate_data["text"] = text
        validate_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        pprint(validate_data["file_name"])

        Certificate.objects.filter(pk=certificate.id).update(
            text=validate_data["text"], status="P")

        CertificateData.objects.create(
            certificate_id=certificate.id, house=validate_data["main_person"].address)
        validate_data["coval"] = coval.id
        validate_data["change"] = change.id

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validate_data, "id": certificate.id, "file": certificate.file}


class CertificateModelAutoModCovalSerializer(ModelSerializer):
    # instituition = serializers.IntegerField()

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",  # Get the address from person object, update it every time you create new cv
            "secondary_person",
            # "instituition",
        ]


class CertificateModelLicBarracaCreateSerializer(ModelSerializer):

    object = serializers.CharField()
    street = serializers.IntegerField()
    file = serializers.FileField(read_only=True)
    range = serializers.CharField()
    

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",
            "secondary_person",
            "object",
            "street",
            "file",
            "range",
        ]

    def validate_object(self, object):
        if not object:
            raise serializers.ValidationError({'object': "Type the object"})
        return object

    def validate_street(self, street):
        if not street:
            raise serializers.ValidationError({'street': "Select street"})
        elif not Street.objects.filter(id=street).exists():
            raise serializers.ValidationError(
                {'street': "This street is not valid"})
        return street

    @atomic()
    def update(self, instance, validated_data):
        # pprint(validated_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validated_data = dict()
        validated_data["number"] = get_number(current_year, certificates, instance,self.context['type_id'])
        validated_data["type_id"] = type_id = int(self.context['type_id'])
        validated_data["status"] = "P"
        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validated_data.copy()

        del new_validate_data["object"]
        del new_validate_data["street"]
        del new_validate_data["range"]

        pprint(validated_data)
        certificate = super().update(instance, new_validate_data)
        object = validated_data["object"]
        validated_data["street"] = street = Street.objects.filter(
            id=validated_data["street"]).first()
        
        if validated_data["type_id"] == 27:
            # del new_validated_data["range"]

            validated_data["range"] = CertificateRange.objects.get(type=validated_data["range"])

        model = AutoModCovalAndLicBarraca(DocumentData(
            validated_data["main_person"], validated_data, certificate, validated_data["secondary_person"]))
        # pprint( StringHelper.renderText(model))
        text, file_name, status = StringHelper.renderText(model)

        validated_data["text"] = text
        validated_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        pprint(validated_data["file_name"])

        # Certificate.objects.update(certificate,text=validated_data["text"])
        Certificate.objects.filter(pk=certificate.id).update(
            text=validated_data["text"], status="P")

        CertificateData.objects.filter(pk=certificate.id).update(
            house=validated_data["main_person"].address)

        validated_data["street"] = street.id

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):

        # pprint(validate_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validate_data = dict()
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = type_id = int(self.context['type_id'])

        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validate_data.copy()

        del new_validate_data["object"]
        del new_validate_data["street"]
        del new_validate_data["range"]

        certificate = super().create(new_validate_data)
        # pprint(validate_data)
        # pprint(validate_data["instituition"])

        object = validate_data["object"]
        validate_data["street"] = street = Street.objects.filter(
            id=validate_data["street"]).first()
        
        if validate_data["type_id"] == 27:
            # del new_validate_data["range"]

            validate_data["range"] = CertificateRange.objects.get(type=validate_data["range"])

        model = AutoModCovalAndLicBarraca(DocumentData(
            validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        # pprint( StringHelper.renderText(model))
        text, file_name, status = StringHelper.renderText(model)

        validate_data["text"] = text
        validate_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        pprint(validate_data["file_name"])

        Certificate.objects.filter(pk=certificate.id).update(
            text=validate_data["text"], status="P")

        CertificateData.objects.create(
            certificate_id=certificate.id, house=validate_data["main_person"].address)

        validate_data["street"] = street.id

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validate_data, "id": certificate.id, "file": certificate.file}


class CertificateModelLicBarracaSerializer(ModelSerializer):
    # instituition = serializers.IntegerField()

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",  # Get the address from person object, update it every time you create new cv
            "secondary_person",
            # "instituition",
        ]


class CertificateModelAutoConstrucaoCreateSerializer(ModelSerializer):

    building_type = serializers.IntegerField()
    street = serializers.IntegerField()
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",
            "secondary_person",
            # "house",
            "building_type",
            "street",
            "file"
        ]

    def validate_building_type(self, building_type):
        if not building_type:
            raise serializers.ValidationError(
                {'building_type': "Select building_type"})
        elif not BiuldingType.objects.filter(id=building_type).exists():
            raise serializers.ValidationError(
                {'building_type': "This building_type is not valid"})
        return building_type

    def validate_street(self, street):
        if not street:
            raise serializers.ValidationError({'street': "Select street"})
        elif not Street.objects.filter(id=street).exists():
            raise serializers.ValidationError(
                {'street': "This street is not valid"})
        return street

    @atomic()
    def update(self, instance, validated_data):
        # pprint(validated_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validated_data = dict()
        validated_data["number"] = get_number(current_year, certificates, instance,self.context['type_id'])
        validated_data["type_id"] = type_id = int(self.context['type_id'])
        validated_data["status"] = "P"
        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validated_data.copy()

        del new_validate_data["building_type"]
        del new_validate_data["street"]

        pprint(validated_data)
        certificate = super().update(instance, new_validate_data)

        validated_data["building_type"] = building_type = BiuldingType.objects.filter(
            id=validated_data["building_type"]).first()
        validated_data["street"] = street = Street.objects.filter(
            id=validated_data["street"]).first()

        model = AutoConstrucao(DocumentData(
            validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))
        # pprint( StringHelper.renderText(model))
        text, file_name, status = StringHelper.renderText(model)

        validated_data["text"] = text
        validated_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        pprint(validated_data["file_name"])

        # Certificate.objects.update(certificate,text=validated_data["text"])
        Certificate.objects.filter(pk=instance.id).update(
            text=validated_data["text"], status="P")

        CertificateData.objects.filter(pk=instance.id).update(
            house=validated_data["main_person"].address)

        validated_data["building_type"] = building_type.id
        validated_data["street"] = street.id

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):

        # pprint(validate_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validate_data = dict()
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = type_id = int(self.context['type_id'])

        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validate_data.copy()
        del new_validate_data["building_type"]
        del new_validate_data["street"]

        certificate = super().create(new_validate_data)
        # pprint(validate_data)
        # pprint(validate_data["instituition"])
        validate_data["building_type"] = building_type = BiuldingType.objects.filter(
            id=validate_data["building_type"]).first()
        validate_data["street"] = street = Street.objects.filter(
            id=validate_data["street"]).first()

        model = AutoConstrucao(DocumentData(
            validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        # pprint( StringHelper.renderText(model))
        text, file_name, status = StringHelper.renderText(model)

        validate_data["text"] = text
        validate_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        pprint(validate_data["file_name"])

        Certificate.objects.filter(pk=certificate.id).update(
            text=validate_data["text"], status="P")

        CertificateData.objects.create(
            certificate_id=certificate.id, house=validate_data["main_person"].address)
        validate_data["building_type"] = building_type.id
        validate_data["street"] = street.id

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validate_data, "id": certificate.id, "file": certificate.file}


class CertificateModelAutoConstrucaoSerializer(ModelSerializer):

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",
            "secondary_person",
            "house",
        ]


class CertificateModelSeventhCreateSerializer(ModelSerializer):

    years = serializers.IntegerField()
    country = serializers.IntegerField(allow_null=True)

    file = serializers.FileField(read_only=True)

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",
            "secondary_person",
            "house",
            "years",
            "country",
            "file"
        ]

    # def validate_institution(self, institution):
    #     if not institution:
    #         raise serializers.ValidationError({'institution': "Select instituition"})
    #     elif not Instituition.objects.filter(id=institution).exists():
    #         raise serializers.ValidationError({'institution': "This instituition is not valid"})
    #     return institution

    @atomic()
    def update(self, instance, validated_data):
        # pprint(validated_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validated_data = dict()
        validated_data["number"] = get_number(current_year, certificates, instance,self.context['type_id'])
        validated_data["type_id"] = type_id = int(self.context['type_id'])
        validated_data["status"] = "P"
        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validated_data.copy()

        del new_validate_data["years"]
        del new_validate_data["country"]

        pprint(validated_data)
        certificate = super().update(instance, new_validate_data)

        validated_data["country"] = country = Country.objects.filter(
            id=validated_data["country"]).first()
        # validated_data["instituition"] = instituition = Instituition.objects.filter(id=validated_data["instituition"]).first()

        model = AtestadoSeventh(DocumentData(
            validated_data["main_person"], validated_data, instance, validated_data["secondary_person"]))
        # pprint( StringHelper.renderText(model))
        text, file_name, status = StringHelper.renderText(model)

        validated_data["text"] = text
        validated_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        pprint(validated_data["file_name"])

        # Certificate.objects.update(certificate,text=validated_data["text"])
        Certificate.objects.filter(pk=instance.id).update(
            text=validated_data["text"], status="P")

        CertificateData.objects.filter(pk=instance.id).update(
            house=validated_data["main_person"].address)

        validated_data["country"] = country.id if country else None

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):

        # pprint(validate_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validate_data = dict()
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = int(self.context['type_id'])

        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validate_data.copy()

        del new_validate_data["years"]
        del new_validate_data["country"]

        certificate = super().create(new_validate_data)
        # pprint(validate_data)
        # pprint(validate_data["instituition"])
        validate_data["country"] = country = Country.objects.filter(
            id=validate_data["country"]).first()
        # validate_data["instituition"] = instituition = Instituition.objects.filter(id=validate_data["instituition"]).first()

        model = AtestadoSeventh(DocumentData(
            validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        # pprint( StringHelper.renderText(model))
        text, file_name, status = StringHelper.renderText(model)

        validate_data["text"] = text
        validate_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        pprint(validate_data["file_name"])

        Certificate.objects.filter(pk=certificate.id).update(
            text=validate_data["text"], status="P")

        CertificateData.objects.create(
            certificate_id=certificate.id, house=validate_data["main_person"].address)
        validate_data["country"] = country.id if country else None

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validate_data, "id": certificate.id, "file": certificate.file}


class CertificateModelSeventhSerializer(ModelSerializer):
    # instituition = serializers.IntegerField()

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",  # Get the address from person object, update it every time you create new cv
            "secondary_person",
            "house",  # house that this person used in this especific certificare
            # "instituition",
        ]


class CertificateModelLicencaBuffetCreateSerializer(ModelSerializer):

    infra = serializers.CharField()
    street = serializers.IntegerField()
    metros = serializers.IntegerField(allow_null=True)
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",
            "secondary_person",
            "infra",
            "street",
            "metros",
            "file",

        ]

    # def validate_institution(self, institution):
    #     if not institution:
    #         raise serializers.ValidationError({'institution': "Select instituition"})
    #     elif not Instituition.objects.filter(id=institution).exists():
    #         raise serializers.ValidationError({'institution': "This instituition is not valid"})
    #     return institution

    @atomic()
    def update(self, instance, validated_data):
        # pprint(validated_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        certificates = Certificate.objects.filter(
            type_id=self.context['type_id'], date_issue__year=current_year)
        # validated_data = dict()
        validated_data["number"] = get_number(current_year, certificates, instance,self.context['type_id'])
        validated_data["type_id"] = type_id = int(self.context['type_id'])
        validated_data["status"] = "P"
        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validated_data.copy()

        del new_validate_data["infra"]
        del new_validate_data["street"]
        del new_validate_data["metros"]

        pprint(validated_data)
        certificate = super().update(instance, new_validate_data)

        validated_data["street"] = street = Street.objects.filter(
            id=validated_data["street"]).first()
        # user
        validated_data["last_date"] = CertificateDate.objects.filter(
            type_id=type_id).order_by('-date').first().date
        validated_data["dates"] = CertificateDate.objects.filter(
            type_id=type_id).order_by('-date')

        model = LicencaBufett(DocumentData(
            validated_data["main_person"], validated_data, certificate, validated_data["secondary_person"]))
        # pprint( StringHelper.renderText(model))
        text, file_name, status = StringHelper.renderText(model)

        validated_data["text"] = text
        validated_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        pprint(validated_data["file_name"])

        # Certificate.objects.update(certificate,text=validated_data["text"])
        Certificate.objects.filter(pk=instance.id).update(
            text=validated_data["text"], status="P")

        CertificateData.objects.filter(pk=instance.id).update(
            house=validated_data["main_person"].address)

        validated_data["street"] = street.id if street else None

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validated_data, "id": certificate.id, "file": certificate.file}

    @atomic()
    def create(self, validate_data):

        # pprint(validate_data)

        # set the number and type,
        # set and save the text in text dev  mode

        current_year = date.today().year
        type_id = int(self.context['type_id'])
        certificates = Certificate.objects.filter(
            type_id=type_id, date_issue__year=current_year)
        # validate_data = dict()
        validate_data["number"] = set_number(current_year, self.context['type_id'])
        validate_data["type_id"] = int(type_id)

        text_helper = StringHelper()
        # pprint(validate_data)
        new_validate_data = validate_data.copy()

        del new_validate_data["infra"]
        del new_validate_data["street"]
        del new_validate_data["metros"]

        certificate = super().create(new_validate_data)

        validate_data["street"] = street = Street.objects.filter(
            id=validate_data["street"]).first()
        # user
        validate_data["last_date"] = CertificateDate.objects.filter(
            type_id=type_id).order_by('-date').first().date
        validate_data["dates"] = CertificateDate.objects.filter(
            type_id=type_id).order_by('-date')

        model = LicencaBufett(DocumentData(
            validate_data["main_person"], validate_data, certificate, validate_data["secondary_person"]))
        # pprint( StringHelper.renderText(model))
        text, file_name, status = StringHelper.renderText(model)

        validate_data["text"] = text
        validate_data["file_name"] = f"/media/certificates/{file_name}.pdf"
        # pprint(validate_data["file_name"])

        Certificate.objects.filter(pk=certificate.id).update(
            text=validate_data["text"], status="P")

        CertificateData.objects.create(
            certificate_id=certificate.id, house=validate_data["main_person"].address)
        validate_data["street"] = street.id if street else None

        certificate = Certificate.objects.get(pk=certificate.id)

        return {**validate_data, "id": certificate.id, "file": certificate.file}


class CertificateModelLicencaBuffetSerializer(ModelSerializer):
    # instituition = serializers.IntegerField()

    class Meta:
        model = Certificate
        fields = [
            "id",
            "main_person",  # Get the address from person object, update it every time you create new cv
            "secondary_person",
        ]


class CertificateTypesSerializer(ModelSerializer):
    # Residence certificate
    # all certificate

    class Meta:
        model = CertificateTypes
        fields = [
            "id",
            "name",
            "gender",
            "slug",
        ]


class CertificateTitleSerializer(ModelSerializer):
    # Residence certificate
    # all certificate

    certificate_type = CertificateTypesSerializer()

    class Meta:
        model = CertificateTitle
        fields = [
            "id",
            "certificate_type",
            "type_price",
            "name",
            "goal"  # house that this person used in this especific certificare
        ]


class CovalSetUpSerializer(ModelSerializer):
    # Residence certificate
    # all certificate
    done = serializers.BooleanField(read_only=True)

    class Meta:
        model = Coval
        fields = [
            "id",
            "done",

        ]

    def create(self, validate_data):
        covals = Coval.objects.order_by("square", "date_used")
        count = 1
        square = covals[0].square
        for coval in covals:
            if coval.square != square:
                square = coval.square
                count = 1

            coval.number = f"{count}-{coval.date_used.year} {coval.square}"
            coval.save()
            count = count + 1
            # Coval.objects.update({"id":coval.id, "number": number})

        return {"done": True}


class CertificateSimplePersonSerializer(ModelSerializer):

    # user = serializers.IntegerField(read_only=True)
    type = CertificateTitleSerializer(read_only=True)

    class Meta:
        model = CertificateSimplePerson
        fields = [
            "id",
            "name",
            "birth_date",
            "gender",
            # "user",
            "type"
        ]

    def create(self, validate_data):

        # validate_data["user_id"] = self.context['user_id']
        validate_data["type_id"] = int(self.context['type_id'])

        return super().create(validate_data)


class CertificateSimplePersonReadOnlySerializer(ModelSerializer):

    # user = serializers.IntegerField(read_only=True)
    type = serializers.CharField(read_only=True)

    class Meta:
        model = CertificateSimplePerson
        fields = [
            "id",
            "name",
            "birth_date",
            "gender",
            # "user",
            "type"
        ]

    def create(self, validate_data):

        # validate_data["user_id"] = self.context['user_id']
        validate_data["type_id"] = int(self.context['type_id'])

        return super().create(validate_data)





class CertificateSimpleParentSerializer(ModelSerializer):

    type = CertificateTitleSerializer(read_only=True)

    class Meta:
        model = CertificateSimpleParent
        fields = [
            "id",
            "name",
            "birth_date",
            # "gender",
            "parent",
            # "user",
            "type"
        ]

    def create(self, validate_data):

        # validate_data["user_id"] = self.context['user_id']
        validate_data["type_id"] = int(self.context['type_id'])

        return super().create(validate_data)


class ParentSerializer(ModelSerializer):

    class Meta:
        model = Parent
        fields = [
            "id",
            "title",
        ]


class CertificateDateSerializer(ModelSerializer):

    # user = serializers.IntegerField(read_only=True)
    type = CertificateTitleSerializer(read_only=True)

    class Meta:
        model = CertificateDate
        fields = [
            "id",
            "date",
            "type"

        ]

    def create(self, validate_data):

        # validate_data["user_id"] = self.context['user_id']
        validate_data["type_id"] = int(self.context['type_id'])

        return super().create(validate_data)


class CertificateSinglePersonSerializer(ModelSerializer):

    # user = serializers.IntegerField(read_only=True)
    type = CertificateTitleSerializer(read_only=True)

    class Meta:
        model = CertificateSinglePerson
        fields = [
            "id",
            "name",
            "gender",
            # "user",
            "type"
        ]

    def create(self, validate_data):

        # removel all saved by current user and add next
        CertificateSinglePerson.objects.filter(
            type_id=self.context['type_id']).delete()
        # CertificateSinglePerson.objects.filter(type_id=self.context['type_id'], user_id=self.context['user_id']).delete() # removel all saved by current user and add next
        # validate_data["user_id"] = self.context['user_id']
        validate_data["type_id"] = int(self.context['type_id'])

        return super().create(validate_data)


class CertificateSerializer(ModelSerializer):

    type = CertificateTitleSerializer()
    main_person = PersonSerializer()
    secondary_person = PersonSerializer()
    house = HouseSerializer()

    # SerializerMethodField(method_name="
    status_detail = serializers.SerializerMethodField(
        method_name="get_status_detail")

    class Meta:
        model = Certificate
        fields = [
            "id",
            "type",
            "number",
            "main_person",
            "secondary_person",
            "date_issue",
            "file",
            "text",
            "house",
            "status",
            "status_detail",
            "obs",
            # "atestado_state",
        ]

    def get_status_detail(self, certificate: Certificate):
        if certificate.status == "R":
            return "Revisto"
        elif certificate.status == "C":
            return "Concluído"
        elif certificate.status == "F":
            return "Incorrecto"
        elif certificate.status == "A":
            return "Arquivado"

        return "Pendente"


class CertificateCommentSerializer(ModelSerializer):

    class Meta:
        model = Certificate
        fields = [
            "id",
            "obs",

        ]


class CertificateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Certificate
        fields = [
            "id",
            "status"
        ]


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

# class CartSerializer(ModelSerializer):
#     weigth = WeigthSerializer()
#     country_from = CountrySerializer()
#     country_to = CountrySerializer()

#     class Meta:
#         model = Cart
#         fields = [
#             "id",
#             "weigth",
#             "country_from",
#             "country_to",
#         ]


# class CartCreateSerializer(ModelSerializer):
#     id = serializers.UUIDField(read_only=True)
#     weigth_id = serializers.IntegerField()
#     country_from_id = serializers.IntegerField()
#     country_to_id = serializers.IntegerField()

#     class Meta:
#         model = Cart
#         fields = [
#             "id",
#             "weigth_id",
#             "country_from_id",
#             "country_to_id",
#         ]


# class AddressFromSerializer(ModelSerializer):
#     cart_id = serializers.UUIDField()

#     class Meta:
#         model = AddressFrom
#         fields = [
#             "id",
#             "cart_id",
#             "house_number",
#             "street",
#             "post_code",
#         ]


# class AddressFromSavedSerializer(ModelSerializer):
#     cart_id = serializers.UUIDField()
#     address_id = serializers.IntegerField()

#     class Meta:
#         model = AddressFrom
#         fields = [
#             "id",
#             "cart_id",
#             "address_id",
#         ]

#     def create(self, validated_data):
#         validated_data["customer_id"] = self.context["customer_id"]

#         customer_addresses = CustomerAddress.objects.filter(
#             customer_id=validated_data["customer_id"], id=validated_data["address_id"]
#         )
#         if not customer_addresses:
#             raise serializers.ValidationError(
#                 {"address": "This address is not correct"}
#             )

#         customer_address = customer_addresses.first()
#         address = dict()
#         address["house_number"] = customer_address.house_number
#         address["street"] = customer_address.street
#         address["post_code"] = customer_address.post_code
#         address["cart_id"] = validated_data["cart_id"]

#         address_from = super().create(address)
#         return {
#             "cart_id": validated_data["cart_id"],
#             "address_id": address_from.id,
#         }


# class AddressToSavedSerializer(ModelSerializer):
#     cart_id = serializers.UUIDField()
#     address_id = serializers.IntegerField()

#     class Meta:
#         model = AddressTo
#         fields = [
#             "id",
#             "cart_id",
#             "address_id",
#         ]

#     def create(self, validated_data):
#         validated_data["customer_id"] = self.context["customer_id"]

#         receivers = Receiver.objects.filter(
#             customer_id=validated_data["customer_id"], id=validated_data["address_id"]
#         )
#         if not receivers:
#             raise serializers.ValidationError(
#                 {"receiver": "This receiver is not correct"}
#             )

#         receiver = receivers.first()
#         address = dict()
#         address["receiver_name"] = receiver.name
#         address["receiver_phone"] = receiver.phone
#         address["house_number"] = receiver.house_number
#         address["street"] = receiver.street
#         address["post_code"] = receiver.post_code
#         address["cart_id"] = validated_data["cart_id"]

#         address_to = super().create(address)
#         return {
#             "cart_id": validated_data["cart_id"],
#             "address_id": address_to.id,
#         }


# class AddressToSerializer(ModelSerializer):
#     cart_id = serializers.UUIDField()

#     class Meta:
#         model = AddressTo
#         fields = [
#             "id",
#             "cart_id",
#             "receiver_name",
#             "receiver_phone",
#             "house_number",
#             "street",
#             "post_code",
#         ]


# class AirportSerializer(ModelSerializer):
#     country = CountrySerializer()

#     class Meta:
#         model = Airport
#         fields = [
#             "id",
#             "country",
#             "name",
#         ]


# class FligthsCompanySerializer(ModelSerializer):
#     class Meta:
#         model = FligthsCompany
#         fields = [
#             "id",
#             "name",
#         ]


# class ReceiverSerializer(ModelSerializer):
#     country = CountrySerializer()

#     class Meta:
#         model = Receiver
#         fields = [
#             "id",
#             "name",
#             "phone",
#             "country",
#             "street",
#             "post_code",
#         ]


# class ReceiverCreateSerializer(ModelSerializer):
#     class Meta:
#         model = Receiver
#         fields = [
#             "id",
#             "name",
#             "phone",
#             "country",
#             "street",
#             "post_code",
#         ]

#     def create(self, validated_data):
#         validated_data["customer_id"] = self.context["customer_id"]
#         return super().create(validated_data)


# class CustomerAddressCreateSerializer(ModelSerializer):
#     class Meta:
#         model = CustomerAddress
#         fields = [
#             "id",
#             "country",
#             "house_number",
#             "street",
#             "post_code",
#         ]

#     @atomic()
#     def create(self, validated_data):
#         validated_data["customer_id"] = self.context["customer_id"]
#         validated_data["post_code"] = validated_data["post_code"].replace(" ", "")
#         customer_address = CustomerAddress.objects.filter(
#             customer_id=validated_data["customer_id"],
#             post_code=validated_data["post_code"],
#         )
#         if not customer_address:
#             self.instance = super().create(validated_data)

#         return customer_address.first()


# class CustomerAddressSerializer(ModelSerializer):
#     country = CountrySerializer()

#     class Meta:
#         model = CustomerAddress
#         fields = [
#             "id",
#             "country",
#             "house_number",
#             "street",
#             "post_code",
#         ]


# class CustomerSerializer(ModelSerializer):
#     first_name = serializers.SerializerMethodField(method_name="get_first_name")
#     last_name = serializers.SerializerMethodField(method_name="get_last_name")
#     address = CustomerAddressSerializer(many=True)

#     # parcels = ParcelSerializer(many=True)
#     # fligths = FligthSerializer(many=True)
#     class Meta:
#         model = Customer
#         fields = [
#             "id",
#             "user",
#             "first_name",
#             "last_name",
#             "address",
#             "parcels",
#             "fligths",
#             # "colaborator_get",
#             # "shippiment_from",
#             # "shippiment_to",
#             "bank_iban",
#         ]

#     def get_first_name(self, customer: Customer):
#         return customer.user.first_name

#     def get_last_name(self, customer: Customer):
#         return customer.user.last_name


# class CustomerUpdateSerializer(ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = [
#             "id",
#             # "colaborator_get",
#             # "shippiment_from",
#             # "shippiment_to",
#             "bank_iban",
#         ]


# class ColaboratorSerializer(ModelSerializer):
#     customer = CustomerSerializer()

#     class Meta:
#         model = Colaborator
#         fields = [
#             "id",
#             # "colaborator_get",
#             # "shippiment_from",
#             # "shippiment_to",
#             "customer",
#         ]


# # class TagSerializer(ModelSerializer):

# #     class Meta:
# #         model = ProductTag
# #         fields = ["id", "tag"]


# class ParcelSerializer(ModelSerializer):
#     weigth = WeigthSerializer()
#     customer = CustomerSerializer()
#     receiver = ReceiverSerializer()
#     colaborator_deliver = ColaboratorSerializer()
#     colaborator_get = ColaboratorSerializer()

#     address_from = CustomerAddressSerializer()

#     # status = serializers.MethodField(method_name="get_status")
#     class Meta:
#         model = Parcel
#         fields = [
#             "id",
#             "customer",
#             "weigth",
#             "status",
#             "created_at",
#             "price",
#             "colaborator_get",
#             "date_collection",
#             "receiver",
#             "address_from",
#             "colaborator_deliver",
#         ]

#     # def get_status(self, parcel: Parcel):
#     #     return parcel.status == "P"


# class ParcelCreateSerializer(ModelSerializer):
#     parcel = ParcelSerializer(read_only=True)
#     cart_id = serializers.UUIDField()

#     class Meta:
#         model = Parcel
#         fields = [
#             "cart_id",
#             "parcel",
#         ]

#     def create(self, validated_data):
#         customer_id = validated_data["customer_id"] = self.context["customer_id"]

#         cart = Cart.objects.filter(id=validated_data["cart_id"]).first()
#         if not cart:
#             raise serializers.ValidationError({"cart": "This cart does not exists"})
#         # verifica se o customer ter este receiver

#         address_from = AddressFrom.objects.filter(cart_id=cart.id).first()
#         address_to = AddressTo.objects.filter(cart_id=cart.id).first()

#         customer_address = CustomerAddress.objects.filter(
#             country_id=cart.country_from.id,
#             street=address_from.street,
#             post_code=address_from.post_code,
#             customer_id=customer_id,
#         ).first()
#         if not customer_address:
#             customer_address = CustomerAddress.objects.create(
#                 country_id=cart.country_from.id,
#                 house_number=address_from.house_number,
#                 street=address_from.street,
#                 post_code=address_from.post_code,
#                 customer_id=customer_id,
#             )

#         receiver = Receiver.objects.filter(
#             name=address_to.receiver_name,
#             phone=address_to.receiver_phone,
#             country_id=cart.country_from.id,
#             house_number=address_to.house_number,
#             street=address_to.street,
#             post_code=address_to.post_code,
#             customer_id=customer_id,
#         ).first()
#         if not receiver:
#             receiver = Receiver.objects.create(
#                 name=address_to.receiver_name,
#                 phone=address_to.receiver_phone,
#                 country_id=cart.country_from.id,
#                 street=address_to.street,
#                 post_code=address_to.post_code,
#                 customer_id=customer_id,
#             )

#         parcel = Parcel.objects.create(
#             customer_id=customer_id,
#             weigth_id=cart.weigth.id,
#             price=cart.weigth.quantity * settings.PRICE_PARCEL_BY_KG,
#             receiver_id=receiver.id,
#             address_from_id=customer_address.id,
#         )

#         cart.delete()

#         return {"cart_id": "", "parcel": parcel}


# class FligthSerializer(ModelSerializer):
#     customer = CustomerSerializer()
#     departure_from = AirportSerializer()
#     arrive_to = AirportSerializer()
#     company = FligthsCompanySerializer()

#     class Meta:
#         model = Fligth
#         fields = [
#             "id",
#             "customer",
#             "weigth",
#             "status",
#             "created_at",
#             "departure_at",
#             "arrive_at",
#             "departure_from",
#             "arrive_to",
#             "number",
#             "company",
#             "price",
#             "payment_status",
#         ]


# class FligthCreateSerializer(ModelSerializer):
#     class Meta:
#         model = Fligth
#         fields = [
#             "id",
#             "weigth",
#             "departure_at",
#             "arrive_at",
#             "departure_from",
#             "arrive_to",
#             "number",
#             "company",
#         ]

#     def create(self, validated_data):
#         validated_data["customer_id"] = self.context["customer_id"]
#         weigth = Weigth.objects.get(id=validated_data["weigth"].id)
#         validated_data["price"] = weigth.quantity * settings.PRICE_FLIGTH_BY_KG

#         return super().create(validated_data)

#     def update(self, instance, validated_data):
#         weigth = Weigth.objects.get(id=validated_data["weigth"].id)
#         validated_data["price"] = weigth.quantity * settings.PRICE_FLIGTH_BY_KG
#         return super().update(instance, validated_data)


# class FligthUpdateSerializer(ModelSerializer):
#     departure_from_id = serializers.IntegerField()
#     arrive_to_id = serializers.IntegerField()
#     company_id = serializers.IntegerField()

#     class Meta:
#         model = Fligth
#         fields = [
#             "id",
#             "weigth",
#             "departure_at",
#             "arrive_at",
#             "departure_from_id",
#             "arrive_to_id",
#             "number",
#             "company_id",
#         ]

#     def update(self, instance, validated_data):
#         weigth = Weigth.objects.get(id=validated_data["weigth"].id)
#         validated_data["price"] = Decimal(weigth.quantity) * Decimal(
#             settings.PRICE_FLIGTH_BY_KG
#         )
#         return super().update(instance, validated_data)


# class ShippimentFligthSerializer(ModelSerializer):
#     parcel = ParcelSerializer()
#     fligth = FligthSerializer()
#     colaborator_to = CustomerSerializer()
#     colaborator_from = CustomerSerializer()

#     class Meta:
#         model = ShippimentFligth
#         fields = [
#             "id",
#             "parcel",
#             "fligth",
#             "created_at",
#             "colaborator_from",
#             "colaborator_to",
#         ]


# class ShippimentFligthCreateSerializer(ModelSerializer):
#     class Meta:
#         model = ShippimentFligth
#         fields = [
#             "id",
#             "parcel",
#             "fligth",
#         ]

#     def create(self, validated_data):
#         validated_data["colaborator_from_id"] = self.context["colaborator_from_id"]
#         return super().create(validated_data)


# class ShippimentFligthUpdateSerializer(ModelSerializer):
#     class Meta:
#         model = ShippimentFligth
#         fields = [
#             "id",
#         ]

#     def update(self, instance, validated_data):
#         validated_data["colaborator_to_id"] = self.context["colaborator_to_id"]

#         return super().update(instance, validated_data)


# class MessagesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Messages
#         fields = ["name", "email", "text"]

#     def create(self, validated_data):
#         # settings.AUTH_USER_MODEL
#         # user_sections = UserSection.objects.filter(section_id=validated_data['subject'])
#         # User = apps.get_model(app_label="core", model_name="User")
#         # users = User.objects.filter(usersection__section=validated_data["subject"])
#         try:
#             # send_mail('subject', 'message', 'edmilbe@gmail.com', ['bob@moshbuy.com'])
#             # mail_admins('subject', 'message', html_message='message')
#             # message = EmailMessage('subject', 'message', 'edmilbe@gmail.com', ['bob@moshbuy.com'])
#             # message.attach_file("core/static/images/contact-us.png")
#             # message.send()
#             validated_data["sent"] = True
#             message = BaseEmailMessage(
#                 template_name="emails/hello.html",
#                 context={
#                     "text": validated_data["text"],
#                     "name": validated_data["name"],
#                     "email": validated_data["email"],
#                 },
#             )
#             message.send([settings.DEFAULT_FROM_EMAIL])
#             return super().create(validated_data)

#         except BadHeaderError:
#             pass
