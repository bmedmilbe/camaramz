from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

class CustomerQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related("user__tenant")

class Customer(models.Model):
    objects = CustomerQuerySet.as_manager()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    level = models.IntegerField(default=1, null=True)
    backstaff = models.BooleanField(default=False)
    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    code = models.IntegerField(null=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Parent(models.Model):
    title = models.CharField(max_length=255)
    in_plural = models.CharField(max_length=255)
    in_plural_mix = models.CharField(max_length=255)
    degree = models.IntegerField(default=1)

    GENDER_MALE = "M"
    GENDER_FEMALE = "F"
    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    ]
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default="M"
    )

    def __str__(self) -> str:
        return f"{self.title}"

class CountyQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related('country')

class County(models.Model):
    objects = CountyQuerySet.as_manager()
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} - {self.country.name}"

class TownQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related('county__country')

class Town(models.Model):
    objects = TownQuerySet.as_manager() 
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.county.name}"

class CemiterioQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related('county__country')

class Cemiterio(models.Model):
    objects = CemiterioQuerySet.as_manager()
    name = models.CharField(max_length=255)

    county = models.ForeignKey(County, on_delete=models.CASCADE)

    
    def __str__(self) -> str:
        return f"{self.name}"


class CovalQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related('cemiterio__county__country')

class Coval(models.Model):
    objects = CovalQuerySet.as_manager()
    nick_number = models.CharField(max_length=255)
    number = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    date_used = models.DateField()
    date_of_deth = models.DateField(null=True, blank=True)
    GENDER_MALE = "M"
    GENDER_FEMALE = "F"
    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    ]
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default=GENDER_MALE
    )
    SQUARE_A = "A"
    SQUARE_B = "B"
    SQUARE_C = "C"
    SQUARE_D = "D"
    SQUARE_CHOICES = [
        (SQUARE_A, "A"),
        (SQUARE_B, "B"),
        (SQUARE_C, "C"),
        (SQUARE_D, "D"),
    ]
    square = models.CharField(
        max_length=1, choices=SQUARE_CHOICES, default=SQUARE_A
    )
    closed = models.BooleanField(default=False)
    selled = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.number}{self.square} | {self.nick_number}"

    cemiterio = models.ForeignKey(
        Cemiterio, on_delete=models.PROTECT, default=1)


class Change(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class BiuldingType(models.Model):
    name = models.CharField(max_length=255)
    prefix = models.CharField(
        max_length=255, default="", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.prefix} {self.name}"

class StreetQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related('town__county__country', 'county__country')

class Street(models.Model):
    objects = StreetQuerySet.as_manager()
    name = models.CharField(max_length=255)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=255)
    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        
        return f"{self.name}"

class HouseQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related('street__town__county__country', 'street__county__country')
class House(models.Model):
    objects = HouseQuerySet.as_manager()
    house_number = models.CharField(max_length=255, null=True)
    street = models.ForeignKey(Street, on_delete=models.CASCADE)

  

    def __str__(self) -> str:
        return f""


class IDType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}"

class PersonBirthAddressQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related('birth_street__town__county__country', 'birth_town__county__country', 'birth_county__country', 'birth_country')
class PersonBirthAddress(models.Model):
    objects = PersonBirthAddressQuerySet.as_manager()
    birth_street = models.ForeignKey(
        Street, on_delete=models.PROTECT, null=True, related_name="birth_person_address")
    birth_town = models.ForeignKey(
        Town, on_delete=models.PROTECT, null=True, related_name="birth_person_address")
    birth_county = models.ForeignKey(
        County, on_delete=models.PROTECT, null=True, related_name="birth_person_address")
    birth_country = models.ForeignKey(
        Country, on_delete=models.PROTECT, related_name="birth_person_address")

    def __str__(self) -> str:
        address = ""
            
        if self.birth_street:
            address = f"{self.birth_street.name}, "
        if self.birth_town:
            address = f"{address}{self.birth_town.name}, "
        if self.birth_county:
            address = f"distrito de {self.birth_county.name}, " if address == "" else f"{address} distrito de {self.birth_county.name}, "

        if self.birth_street != None and self.birth_town != None:
            if self.birth_street.name == self.birth_town.name and self.birth_town.name == self.birth_county.name:
                return f"distrito de {self.birth_county.name}, {self.birth_country.name}"
            if self.birth_street.name == self.birth_town.name:
                return f"{self.birth_street.name}, distrito de {self.birth_county.name}, {self.birth_country.name}"

        address = f"{address}{self.birth_country.name}"

        return f"{address}"


class Instituition(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}"

class PersonQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related(
            'id_type',
            'id_issue_local',
            'id_issue_country',
            'nationality',
            'birth_address',
            'birth_address__birth_street__town__county__country',
            'birth_address__birth_town__county__country',
            'birth_address__birth_county__country',
            'birth_address__birth_country',
            'address__street__town__county__country',
            'address__street__county__country',
        )

class Person(models.Model):
    id = models.AutoField(primary_key=True)
    objects = PersonQuerySet.as_manager()

    name = models.TextField()
    surname = models.TextField(db_index=True)
    id_number = models.TextField(db_index=True)
    
    birth_date = models.DateField(null=True, blank=True, db_index=True)
    birth_day = models.IntegerField(null=True)
    birth_month = models.IntegerField(null=True)
    birth_year = models.IntegerField(null=True)

    bi_nasc_loc = models.IntegerField(null=True)
    birth_address = models.ForeignKey(
        PersonBirthAddress, on_delete=models.CASCADE, related_name="persons", null=True)

    id_type = models.ForeignKey(IDType, on_delete=models.PROTECT)

    id_issue_local = models.ForeignKey(
        Instituition, on_delete=models.PROTECT, related_name="id_issue_person")
    id_issue_country = models.ForeignKey(
        Country, on_delete=models.PROTECT, related_name="id_issue_person", null=True)
    
    id_issue_date = models.DateField(null=True, db_index=True)
    id_issue_day = models.IntegerField(null=True, default=1)
    id_issue_month = models.IntegerField(null=True, default=1)
    id_issue_year = models.IntegerField(null=True, default=1)

    id_expire_date = models.DateField(null=True)
    nationality = models.ForeignKey(
        Country, on_delete=models.PROTECT, related_name="person_nationality", null=True)

    father_name = models.TextField(null=True)
    mother_name = models.TextField(null=True)

    address = models.ForeignKey(
        House, on_delete=models.PROTECT, related_name='person', null=True)

    MARRITIAL_STATUS_MARRIED = "M"
    MARRITIAL_STATUS_SINGLE = "S"
    MARRITIAL_STATUS_LIVING_TOGETHER = "L"
    MARRITIAL_STATUS_VIUVO = "V"
    MARRITIAL_STATUS_DIVOCIED = "D"
    MARRITIAL_STATUS_CHOICES = [
        (MARRITIAL_STATUS_MARRIED, "Married"),
        (MARRITIAL_STATUS_SINGLE, "Single"),
        (MARRITIAL_STATUS_LIVING_TOGETHER, "Living together"),
        (MARRITIAL_STATUS_VIUVO, "Viuvo"),
        (MARRITIAL_STATUS_DIVOCIED, "Divorcied"),
    ]

    bi_estado = models.IntegerField(null=True)
    bi_sexo = models.IntegerField(null=True)

    # Kept TextField here to match your request, but limited by choices
    status = models.TextField(
        choices=MARRITIAL_STATUS_CHOICES, null=True
    )

    GENDER_MALE = "M"
    GENDER_FEMALE = "F"
    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    ]
    gender = models.TextField(
        choices=GENDER_CHOICES, null=True
    )

    class Meta:
        indexes = [
            models.Index(fields=['name', 'surname']),
        ]


    def clean(self):
        super().clean()
        if self.birth_date:
            if self.birth_date > date.today():
                raise ValidationError({
                    'birth_date': "A data de nascimento não pode estar no futuro."
                })
            
    def __str__(self) -> str:
        return f"{self.name} {self.surname} with {self.id_type.name} {self.id_number} from {self.nationality.name if self.nationality != None else '' }"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class CertificateTypes(models.Model):
    name = models.CharField(max_length=255)
    GENDER_MALE = "o"
    GENDER_FEMALE = "a"
    GENDER_CHOICES = [
        (GENDER_MALE, "o"),
        (GENDER_FEMALE, "a"),
    ]
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default=GENDER_MALE, null=True
    )
    slug = models.SlugField(max_length=255, null=True)


    def __str__(self) -> str:
        return f"{self.name}"


class University(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}"


class Ifen(models.Model):
    name = models.CharField(max_length=255)
    size = models.IntegerField()

    def __str__(self) -> str:
        return str(self.size)

class CertificateTitleQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related('certificate_type')

class CertificateTitle(models.Model):
    objects = CertificateTitleQuerySet.as_manager()
    name = models.CharField(max_length=255)  
    certificate_type = models.ForeignKey(
        CertificateTypes, on_delete=models.CASCADE, null=True)
    type_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    goal = models.CharField(max_length=255, null=True, blank=True)  
    slug = models.SlugField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.certificate_type.name} {self.goal} {self.name}"

class CertificateQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related(
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
            'secondary_person__address__street__county__country'
        )


class Certificate(models.Model):
    id = models.AutoField(primary_key=True)

    objects = CertificateQuerySet.as_manager()

    type = models.ForeignKey(
        'CertificateTitle', on_delete=models.PROTECT, null=True, db_index=True)
    
    number = models.TextField(null=True, db_index=True)
    
    status = models.TextField(
        choices=[
            ("C", "Concluído"),
            ("F", "Incorrecto"),
            ("P", "Pendente"),
            ("R", "Revisto"),
            ("A", "Archived"),
        ], 
        default="P", 
        null=True,
        db_index=True 
    )

    date_issue = models.DateTimeField(auto_now=True, null=True, db_index=True)
    
    text = models.TextField(default="", null=True)
    
    main_person = models.ForeignKey(
        'Person', on_delete=models.PROTECT, related_name="main_person_certificates", null=True)
    secondary_person = models.ForeignKey(
        'Person', on_delete=models.PROTECT, null=True, related_name="second_person_certificates")
    house = models.ForeignKey(
        'House', on_delete=models.PROTECT, related_name="certificates", null=True)
    
    file = models.FileField(upload_to='camaramz/certificates', null=True, blank=True)
    obs = models.TextField(null=True)

    atestado_state = models.IntegerField(null=True, default=1)
    type_id1 = models.IntegerField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['number', 'status']),
        ]


    def __str__(self) -> str:
        return f"{self.type.name} {self.number}"


class CertificateSimplePersonQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related('type__certificate_type')

class CertificateSimplePerson(models.Model):
    objects = CertificateSimplePersonQuerySet.as_manager()
    type = models.ForeignKey(CertificateTitle, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    GENDER_MALE = "M"
    GENDER_FEMALE = "F"
    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Femal"),
    ]
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES
    )
    birth_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.name}"

 
class CertificateSimpleParentQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related('type__certificate_type', 'parent')

class CertificateSimpleParent(models.Model):
    objects = CertificateSimpleParentQuerySet.as_manager()
    type = models.ForeignKey(CertificateTitle, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    GENDER_MALE = "M"
    GENDER_FEMALE = "F"
    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    ]

    birth_date = models.DateField()
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}"



class CertificateSinglePersonQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related('type__certificate_type')
class CertificateSinglePerson(models.Model):
    objects = CertificateSinglePersonQuerySet.as_manager()
    type = models.ForeignKey(CertificateTitle, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    GENDER_MALE = "M"
    GENDER_FEMALE = "F"
    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    ]
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES
    )

    def __str__(self) -> str:
        return f"{self.name}"
    
class CertificateRange(models.Model):

    
    TYPE_BASIC = "B"
    TYPE_MEDIUM = "M"
    TYPE_ADVENCED = "C"
    GENDER_CHOICES = [
        (TYPE_BASIC, "Basic"),
        (TYPE_MEDIUM, "Medium"),
        (TYPE_ADVENCED, "Average"),
    ]
    
    type = models.CharField(
        max_length=1, choices=GENDER_CHOICES, unique=True
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)

class CertificateDateQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related('type__certificate_type')

class CertificateDate(models.Model):
    objects = CertificateDateQuerySet.as_manager()
    type = models.ForeignKey(CertificateTitle, on_delete=models.CASCADE)
    date = models.DateField()


class CertificateDataQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related(
            'certificate__type__certificate_type',
            'house__street__town__county__country',
        )


class CertificateData(models.Model):
    objects = CertificateDataQuerySet.as_manager()
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.certificate}"

class CovalSallesQuerySet(models.QuerySet):
    def optimized(self):
        return self.select_related(
            'coval__cemiterio__county__country',
            'person__id_type',
            'person__id_issue_local',
            'person__id_issue_country',
            'person__nationality',
            'person__birth_address',
            'person__birth_address__birth_street__town__county__country',
            'person__birth_address__birth_town__county__country',
            'person__birth_address__birth_county__country',
            'person__birth_address__birth_country',
            'person__address__street__town__county__country',
            'person__address__street__county__country',)

class CovalSalles(models.Model):
    objects = CovalSallesQuerySet.as_manager()
    coval = models.ForeignKey(Coval, on_delete=models.PROTECT)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)

class Messages(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    text = models.TextField()
    sent = models.BooleanField(default=False, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"
