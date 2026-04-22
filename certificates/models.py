from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


class CustomerQuerySet(models.QuerySet):
    """Custom QuerySet for optimizing Customer queries with select_related."""

    def optimized(self):
        """Optimize QuerySet with select_related for user and tenant.

        Returns:
            QuerySet: Optimized queryset with user__tenant selected.
        """
        return self.select_related("user__tenant")


class Customer(models.Model):
    """Represents a customer user with staff status and level."""

    objects = CustomerQuerySet.as_manager()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    level = models.IntegerField(default=1, null=True)
    backstaff = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Return string representation of customer.

        Returns:
            str: First and last name of the customer.
        """
        return f"{self.user.first_name} {self.user.last_name}"


class Country(models.Model):
    """Represents a country with name and code."""

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    code = models.IntegerField(null=True)

    def __str__(self) -> str:
        """Return string representation of country.

        Returns:
            str: Country name.
        """
        return f"{self.name}"


class Parent(models.Model):
    """Represents a parent/sibling relationship with gender designation."""

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
        """Return string representation of parent.

        Returns:
            str: Parent title.
        """
        return f"{self.title}"


class CountyQuerySet(models.QuerySet):
    """Custom QuerySet for optimizing County queries."""

    def optimized(self):
        """Optimize QuerySet by selecting related country.

        Returns:
            QuerySet: Optimized queryset with country relation pre-fetched.
        """
        return self.select_related('country')


class County(models.Model):
    """Represents a county or administrative division within a country.

    Attributes:
        name: County name (max 255 characters).
        slug: URL-friendly slug for the county name.
        country: Foreign key to the parent Country.
    """
    objects = CountyQuerySet.as_manager()
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return string representation of county.

        Returns:
            str: County name and parent country name (format: "County - Country").
        """
        return f"{self.name} - {self.country.name}"


class TownQuerySet(models.QuerySet):
    """Custom QuerySet for optimizing Town queries."""

    def optimized(self):
        """Optimize QuerySet by selecting related county and country.

        Returns:
            QuerySet: Optimized queryset with county__country relations pre-fetched.
        """
        return self.select_related('county__country')


class Town(models.Model):
    """Represents a town or municipality within a county.

    Attributes:
        name: Town name (max 255 characters).
        slug: URL-friendly slug for the town name.
        county: Foreign key to the parent County (nullable).
    """
    objects = TownQuerySet.as_manager()
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        """Return string representation of town.

        Returns:
            str: Town name and parent county name (format: "Town - County").
        """
        return f"{self.name} - {self.county.name}"


class CemiterioQuerySet(models.QuerySet):
    """Custom QuerySet for optimizing Cemiterio (cemetery) queries."""

    def optimized(self):
        """Optimize QuerySet by selecting related county and country.

        Returns:
            QuerySet: Optimized queryset with county__country relations pre-fetched.
        """
        return self.select_related('county__country')


class Cemiterio(models.Model):
    """Represents a cemetery location.

    Attributes:
        name: Cemetery name (max 255 characters).
        county: Foreign key to the County where the cemetery is located.
    """
    objects = CemiterioQuerySet.as_manager()
    name = models.CharField(max_length=255)

    county = models.ForeignKey(County, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return string representation of cemetery.

        Returns:
            str: Cemetery name.
        """
        return f"{self.name}"


class CovalQuerySet(models.QuerySet):
    """Custom QuerySet for optimizing Coval (burial plot) queries."""

    def optimized(self):
        """Optimize QuerySet by selecting related cemetery, county and country.

        Returns:
            QuerySet: Optimized queryset with cemiterio__county__country relations pre-fetched.
        """
        return self.select_related('cemiterio__county__country')


class Coval(models.Model):
    """Represents a burial plot or grave in a cemetery.

    Tracks plot usage history, deceased person information, square location,
    and sale/closure status.

    Attributes:
        nick_number: Nickname or identifier for the plot.
        number: Official plot number (nullable).
        name: Name associated with the plot (nullable).
        date_used: Date when the plot was first used.
        date_of_deth: Date of death of person buried (nullable).
        gender: Gender designation (M/F).
        square: Letter designation of cemetery square (A/B/C/D).
        closed: Whether the plot is permanently closed.
        selled: Whether the plot has been sold.
        cemiterio: Foreign key to the Cemetery.
    """
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
        """Return string representation of burial plot.

        Returns:
            str: Plot number and square with nick number (format: "NumberSquare | NickNumber").
        """
        return f"{self.number}{self.square} | {self.nick_number}"

    cemiterio = models.ForeignKey(
        Cemiterio, on_delete=models.PROTECT, default=1)


class Change(models.Model):
    """Represents a price change or modification fee.

    Attributes:
        name: Description of the change or modification (max 255 characters).
        price: Cost in decimal format (max 6 digits, 2 decimal places).
    """
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class BiuldingType(models.Model):
    """Represents a building or structure type with naming conventions.

    Attributes:
        name: Type name (max 255 characters).
        prefix: Optional prefix for the building type name (max 255 characters, nullable).
    """
    name = models.CharField(max_length=255)
    prefix = models.CharField(
        max_length=255, default="", null=True, blank=True)

    def __str__(self) -> str:
        """Return string representation of building type.

        Returns:
            str: Prefix and name combined (format: "Prefix Name").
        """
        return f"{self.prefix} {self.name}"


class StreetQuerySet(models.QuerySet):
    """Custom QuerySet for optimizing Street queries."""

    def optimized(self):
        """Optimize QuerySet by selecting related town, county, and country.

        Returns:
            QuerySet: Optimized queryset with town__county__country and county__country relations pre-fetched.
        """
        return self.select_related('town__county__country', 'county__country')


class Street(models.Model):
    """Represents a street or road in a town or county.

    Attributes:
        name: Street name (max 255 characters).
        town: Foreign key to Town (nullable).
        slug: URL-friendly slug for the street name.
        county: Foreign key to County (nullable).
    """
    objects = StreetQuerySet.as_manager()
    name = models.CharField(max_length=255)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=255)
    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        """Return string representation of street.

        Returns:
            str: Street name.
        """
        return f"{self.name}"


class HouseQuerySet(models.QuerySet):
    """Custom QuerySet for optimizing House queries."""

    def optimized(self):
        """Optimize QuerySet by selecting related street, town, county and country.

        Returns:
            QuerySet: Optimized queryset with street location relations pre-fetched.
        """
        return self.select_related('street__town__county__country', 'street__county__country')


class House(models.Model):
    """Represents a physical house or address.

    Attributes:
        house_number: House number or address identifier (nullable).
        street: Foreign key to the Street where the house is located.
    """
    objects = HouseQuerySet.as_manager()
    house_number = models.CharField(max_length=255, null=True)
    street = models.ForeignKey(Street, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return string representation of house.

        Returns:
            str: Empty string (placeholder for address display logic).
        """
        return f""


class IDType(models.Model):
    """Represents an identification document type.

    Examples include passport, national ID, driver's license, etc.

    Attributes:
        name: ID type name (max 255 characters).
    """
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        """Return string representation of ID type.

        Returns:
            str: ID type name.
        """
        return f"{self.name}"


class PersonBirthAddressQuerySet(models.QuerySet):
    """Custom QuerySet for optimizing PersonBirthAddress queries."""

    def optimized(self):
        """Optimize QuerySet by selecting all related location hierarchies.

        Returns:
            QuerySet: Optimized queryset with birth location relations pre-fetched.
        """
        return self.select_related('birth_street__town__county__country',
                                   'birth_town__county__country', 'birth_county__country', 'birth_country')


class PersonBirthAddress(models.Model):
    """Represents the birth address/place of a person.

    Stores hierarchical location data for where a person was born,
    including street, town, county, and country information.

    Attributes:
        birth_street: Foreign key to birth Street (nullable).
        birth_town: Foreign key to birth Town (nullable).
        birth_county: Foreign key to birth County (nullable).
        birth_country: Foreign key to birth Country (required).
    """
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
        """Return formatted string representation of birth address.

        Constructs a hierarchical address string based on available location fields,
        handling cases where street, town, and county have the same name specially.

        Returns:
            str: Formatted address string (e.g., "Street, Town, distrito de County, Country").
        """
        address = ""

        if self.birth_street:
            address = f"{self.birth_street.name}, "
        if self.birth_town:
            address = f"{address}{self.birth_town.name}, "
        if self.birth_county:
            address = f"distrito de {self.birth_county.name}, " if address == "" else f"{address} distrito de {self.birth_county.name}, "

        if self.birth_street is not None and self.birth_town is not None:
            if self.birth_street.name == self.birth_town.name and self.birth_town.name == self.birth_county.name:
                return f"distrito de {self.birth_county.name}, {self.birth_country.name}"
            if self.birth_street.name == self.birth_town.name:
                return f"{self.birth_street.name}, distrito de {self.birth_county.name}, {self.birth_country.name}"

        address = f"{address}{self.birth_country.name}"

        return f"{address}"


class Instituition(models.Model):
    """Represents an institution that issues identification documents.

    Examples: passport office, civil registry, police department, etc.

    Attributes:
        name: Institution name (max 255 characters).
    """
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        """Return string representation of institution.

        Returns:
            str: Institution name.
        """
        return f"{self.name}"


class PersonQuerySet(models.QuerySet):
    """Custom QuerySet for optimizing Person queries with comprehensive select_related."""

    def optimized(self):
        """Optimize QuerySet by selecting all related person data hierarchies.

        Pre-fetches ID type, location information, birth address location hierarchy,
        current address location hierarchy, and nationality data.

        Returns:
            QuerySet: Optimized queryset with all person-related relations pre-fetched.
        """
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
    """Represents an individual person with identification and biographical information.

    Stores comprehensive personal data including identification documents, birth information,
    family details, current address, and marital status.

    Attributes:
        name: Person's given name(s).
        surname: Person's family name (indexed).
        id_number: Identification document number (indexed).
        birth_date: Date of birth (indexed, nullable).
        birth_day: Day of birth (1-31, nullable).
        birth_month: Month of birth (1-12, nullable).
        birth_year: Year of birth (nullable).
        bi_nasc_loc: Birth location indicator (nullable).
        birth_address: Foreign key to PersonBirthAddress (nullable).
        id_type: Foreign key to ID type (required).
        id_issue_local: Foreign key to issuing Institution (required).
        id_issue_country: Foreign key to issuing Country (nullable).
        id_issue_date: Date document was issued (indexed, nullable).
        id_issue_day: Day issued (1-31, nullable, default 1).
        id_issue_month: Month issued (1-12, nullable, default 1).
        id_issue_year: Year issued (nullable, default 1).
        id_expire_date: Date document expires (nullable).
        nationality: Foreign key to Country of nationality (nullable).
        father_name: Father's name (nullable).
        mother_name: Mother's name (nullable).
        address: Foreign key to House/current address (nullable).
        status: Marital status (TextField with choices, nullable).
        gender: Gender designation (M/F, TextField with choices, nullable).
        bi_estado: Marital status indicator (nullable).
        bi_sexo: Gender indicator (nullable).
    """
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
        """Validate person data before saving.

        Raises:
            ValidationError: If birth_date is in the future.
        """
        super().clean()
        if self.birth_date:
            if self.birth_date > date.today():
                raise ValidationError({
                    'birth_date': "A data de nascimento não pode estar no futuro."
                })

    def __str__(self) -> str:
        """Return string representation of person.

        Returns:
            str: Person's full name with ID type, number, and nationality.
        """
        return f"{self.name} {self.surname} with {self.id_type.name} {self.id_number} from {self.nationality.name if self.nationality != None else '' }"

    def save(self, *args, **kwargs):
        """Save person to database.

        Calls parent save method to persist changes.
        """
        super().save(*args, **kwargs)


class CertificateTypes(models.Model):
    """Represents a certificate type or category.

    Attributes:
        name: Certificate type name (max 255 characters).
        gender: Grammatical gender designation for Portuguese (o/a).
        slug: URL-friendly slug for the type (nullable).
    """
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
        """Return string representation of certificate type.

        Returns:
            str: Certificate type name.
        """
        return f"{self.name}"


class University(models.Model):
    """Represents an educational institution or university.

    Attributes:
        name: University/institution name (max 255 characters).
    """
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        """Return string representation of university.

        Returns:
            str: University name.
        """
        return f"{self.name}"


class Ifen(models.Model):
    """Represents an IFEN (size/classification) category.

    Attributes:
        name: IFEN name or description (max 255 characters).
        size: Numeric size or classification value.
    """
    name = models.CharField(max_length=255)
    size = models.IntegerField()

    def __str__(self) -> str:
        """Return string representation of IFEN.

        Returns:
            str: String representation of size value.
        """
        return str(self.size)


class CertificateTitleQuerySet(models.QuerySet):
    """Custom QuerySet for optimizing CertificateTitle queries."""

    def optimized(self):
        """Optimize QuerySet by selecting related certificate type.

        Returns:
            QuerySet: Optimized queryset with certificate_type relation pre-fetched.
        """
        return self.select_related('certificate_type')


class CertificateTitle(models.Model):
    """Represents a specific certificate title or variant.

    Maps to a CertificateType with additional metadata like pricing, goal,
    and display slug.

    Attributes:
        name: Certificate title name (max 255 characters).
        certificate_type: Foreign key to CertificateTypes (nullable).
        type_price: Price for this certificate type (nullable, max 12 digits).
        goal: Purpose or goal of the certificate (max 255, nullable).
        slug: URL-friendly slug for the title (nullable).
    """
    objects = CertificateTitleQuerySet.as_manager()
    name = models.CharField(max_length=255)
    certificate_type = models.ForeignKey(
        CertificateTypes, on_delete=models.CASCADE, null=True)
    type_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    goal = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        """Return string representation of certificate title.

        Returns:
            str: Combined certificate type, goal, and name.
        """
        return f"{self.certificate_type.name} {self.goal} {self.name}"


class CertificateQuerySet(models.QuerySet):
    """Custom QuerySet for optimizing Certificate queries with comprehensive relations."""

    def optimized(self):
        """Optimize QuerySet by selecting all related certificate data.

        Pre-fetches certificate title, main person details with locations,
        secondary person details with locations, and house location hierarchy.

        Returns:
            QuerySet: Optimized queryset with all certificate relations pre-fetched.
        """
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
    """Represents an issued certificate document.

    Tracks certificate issuance, status, and associated person/location data
    for document generation and record-keeping.

    Attributes:
        type: Foreign key to CertificateTitle (nullable, indexed).
        number: Certificate number/reference (nullable, indexed).
        status: Certificate status - Concluído/Incorrecto/Pendente/Revisto/Archived (indexed).
        date_issue: Auto-populated date and time of issuance (indexed).
        text: Template text for certificate content (nullable).
        main_person: Foreign key to primary Person (nullable).
        secondary_person: Foreign key to secondary Person (nullable).
        house: Foreign key to House address (nullable).
        file: PDF or document file upload (nullable).
        obs: Observations or notes (nullable).
        atestado_state: State/status indicator (nullable, default 1).
        type_id1: Legacy type identifier (nullable).
    """
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
        """Return string representation of certificate.

        Returns:
            str: Certificate type and number.
        """
        return f"{self.type.name} {self.number}"


class CertificateSimplePersonQuerySet(models.QuerySet):
    """Custom QuerySet for optimizing CertificateSimplePerson queries."""

    def optimized(self):
        """Optimize QuerySet by selecting related certificate type.

        Returns:
            QuerySet: Optimized queryset with type__certificate_type relation pre-fetched.
        """
        return self.select_related('type__certificate_type')


class CertificateSimplePerson(models.Model):
    """Represents a simplified person record for certificate generation.

    Used when full Person details are not needed or available.

    Attributes:
        type: Foreign key to CertificateTitle.
        name: Person's name (max 255 characters).
        gender: Gender designation (M/F).
        birth_date: Date of birth.
    """
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
        """Return string representation of simple person.

        Returns:
            str: Person's name.
        """
        return f"{self.name}"


class CertificateSimpleParentQuerySet(models.QuerySet):
    """Custom QuerySet for optimizing CertificateSimpleParent queries."""

    def optimized(self):
        """Optimize QuerySet by selecting related certificate type and parent.

        Returns:
            QuerySet: Optimized queryset with type__certificate_type and parent relations pre-fetched.
        """
        return self.select_related('type__certificate_type', 'parent')


class CertificateSimpleParent(models.Model):
    """Represents a simplified parent record for certificate generation.

    Combines person information with parent/family relationship designation.

    Attributes:
        type: Foreign key to CertificateTitle.
        name: Parent's name (max 255 characters).
        birth_date: Date of birth.
        parent: Foreign key to Parent (relationship type).
        gender: Gender designation (M/F).
    """
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
        """Return string representation of simple parent.

        Returns:
            str: Parent's name.
        """
        return f"{self.name}"


class CertificateSinglePersonQuerySet(models.QuerySet):
    """Custom QuerySet for optimizing CertificateSinglePerson queries."""

    def optimized(self):
        """Optimize QuerySet by selecting related certificate type.

        Returns:
            QuerySet: Optimized queryset with type__certificate_type relation pre-fetched.
        """
        return self.select_related('type__certificate_type')


class CertificateSinglePerson(models.Model):
    """Represents a single person record for certificate generation.

    Alternative representation of a person for specific certificate types.

    Attributes:
        type: Foreign key to CertificateTitle.
        name: Person's name (max 255 characters).
        gender: Gender designation (M/F).
    """
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
        """Return string representation of single person.

        Returns:
            str: Person's name.
        """
        return f"{self.name}"


class CertificateRange(models.Model):
    """Represents a price range or tier for certificates.

    Used for categorizing certificates by complexity or service level.

    Attributes:
        type: Price range type designation (B/M/C) - unique constraint.
        price: Price amount (max 8 digits, 2 decimal places).
    """
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
    """Custom QuerySet for optimizing CertificateDate queries."""

    def optimized(self):
        """Optimize QuerySet by selecting related certificate type.

        Returns:
            QuerySet: Optimized queryset with type__certificate_type relation pre-fetched.
        """
        return self.select_related('type__certificate_type')


class CertificateDate(models.Model):
    """Represents a date associated with a certificate.

    Used for tracking multiple relevant dates in certificate lifecycle.

    Attributes:
        type: Foreign key to CertificateTitle.
        date: The associated date.
    """
    objects = CertificateDateQuerySet.as_manager()
    type = models.ForeignKey(CertificateTitle, on_delete=models.CASCADE)
    date = models.DateField()


class CertificateDataQuerySet(models.QuerySet):
    """Custom QuerySet for optimizing CertificateData queries."""

    def optimized(self):
        """Optimize QuerySet by selecting related certificate and house location data.

        Returns:
            QuerySet: Optimized queryset with certificate and house location relations pre-fetched.
        """
        return self.select_related(
            'certificate__type__certificate_type',
            'house__street__town__county__country',
        )


class CertificateData(models.Model):
    """Represents auxiliary data linked to a certificate.

    Associates a certificate with specific house/location information.

    Attributes:
        certificate: Foreign key to Certificate.
        house: Foreign key to House (protected).
    """
    objects = CertificateDataQuerySet.as_manager()
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.PROTECT)

    def __str__(self) -> str:
        """Return string representation of certificate data.

        Returns:
            str: Associated certificate information.
        """
        return f"{self.certificate}"


class CovalSallesQuerySet(models.QuerySet):
    """Custom QuerySet for optimizing CovalSalles (burial plot sales) queries."""

    def optimized(self):
        """Optimize QuerySet by selecting related coval and person data with all locations.

        Returns:
            QuerySet: Optimized queryset with coval and person location hierarchies pre-fetched.
        """
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
    """Represents the sale or assignment of a burial plot to a person.

    Tracks ownership/user of burial plots.

    Attributes:
        coval: Foreign key to Coval (burial plot) - protected.
        person: Foreign key to Person (plot owner) - protected.
    """
    objects = CovalSallesQuerySet.as_manager()
    coval = models.ForeignKey(Coval, on_delete=models.PROTECT)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)


class Messages(models.Model):
    """Represents a contact form message or user communication.

    Stores messages submitted by users, typically through a contact form.

    Attributes:
        name: Sender's name (max 255 characters).
        email: Sender's email address.
        text: Message content.
        sent: Whether the message has been sent/processed.
        date: Timestamp of message creation (auto-populated).
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    text = models.TextField()
    sent = models.BooleanField(default=False, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        """Return string representation of message.

        Returns:
            str: Sender's name.
        """
        return f"{self.name}"
