"""Data container for certificate document generation context.

This module provides data structure for passing certificate information
to document generators. Aggregates person records, certificate types,
and form data needed for document rendering.

Classes:
    DocumentData: Container for certificate document context and metadata.
"""

from certificates.models import Person
from certificates.models import Certificate
from certificates.models import CertificateTypes
from certificates.models import CertificateTitle


class DocumentData():
    """Container for certificate document generation data and context.

    Aggregates all necessary information for generating a certificate document,
    including person records (primary and secondary), certificate types/titles,
    validated form data, and related certificate records.

    Attributes:
        bi1 (Person): Primary person (individual) the certificate is for.
        bi2 (Person): Secondary person (e.g., spouse), if applicable.
        type (CertificateTypes): Certificate type classification.
        type2 (CertificateTitle): Specific certificate title/variant.
        data (dict): Validated form data with certificate-specific fields.
        certificate (Certificate): The certificate model instance.
        doc_update_number (int): Reference to related certificate if updating.
    """

    def __init__(self,
                 bi: Person,
                 validated_data,
                 certificate: Certificate,
                 bi2_id=None,
                 certificate2=None):  # Certificate
        """Initialize document data container.

        Args:
            bi (Person): Primary person record.
            validated_data (dict): Validated serializer data with form fields.
            certificate (Certificate): Certificate model instance being generated.
            bi2_id (int, optional): ID number of secondary person. Defaults to None.
            certificate2 (Certificate, optional): Related certificate for updates. Defaults to None.
        """

        self.bi1 = bi
        self.bi2 = Person.objects.filter(id_number=bi2_id).first()
        self.type = CertificateTypes.objects.filter(id=certificate.type.certificate_type.id).first()
        self.type2 = CertificateTitle.objects.filter(id=certificate.type.id).first()
        if certificate2:
            self.doc_update_number = certificate2.id

        self.data = validated_data
        self.certificate = certificate
