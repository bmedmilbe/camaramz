from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

class Customer(models.Model):
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


class County(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} - {self.country.name}"


class Town(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.county.name}"


class Cemiterio(models.Model):
    name = models.CharField(max_length=255)

    county = models.ForeignKey(County, on_delete=models.CASCADE)

    
    def __str__(self) -> str:
        return f"{self.name}"


class Coval(models.Model):
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


class Street(models.Model):
    name = models.CharField(max_length=255)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=255)
    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        
        return f"{self.name}"


class House(models.Model):
    house_number = models.CharField(max_length=255, null=True)
    street = models.ForeignKey(Street, on_delete=models.CASCADE)

  

    def __str__(self) -> str:
        return f""
        return f"{self.house_number} {self.street.name}, {self.street.town.name}, {self.street.town.county.country.name}"


class IDType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}"


class PersonBirthAddress(models.Model):
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

class Person(models.Model):
    id = models.AutoField(primary_key=True)
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


class CertificateTitle(models.Model):

    name = models.CharField(max_length=255)  
    certificate_type = models.ForeignKey(
        CertificateTypes, on_delete=models.CASCADE, null=True)
    type_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    goal = models.CharField(max_length=255, null=True, blank=True)  
    slug = models.SlugField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.certificate_type.name} {self.goal} {self.name}"


class Certificate(models.Model):
    id = models.AutoField(primary_key=True)

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


class CertificateSimplePerson(models.Model):

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

 


class CertificateSimpleParent(models.Model):

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


class CertificateSinglePerson(models.Model):

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

class CertificateDate(models.Model):

    type = models.ForeignKey(CertificateTitle, on_delete=models.CASCADE)
    date = models.DateField()


class CertificateData(models.Model):


    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.certificate}"

class CovalSalles(models.Model):
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
