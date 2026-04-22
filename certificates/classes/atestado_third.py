"""Certificate attestation (Atestado) generation for Model Three documents.

This module implements the Model Three certificate format - an attestation
confirming residency with date-specific conditions (30+ days residency,
specific date requirements).

Classes:
    AtestadoThird: Generator for Model Three certificate documents.
"""

from .pdf import PDF
from .string_helper import StringHelper
from certificates.classes.interfaces.document import Document
from pprint import pprint
from .document_data import DocumentData


class AtestadoThird(Document):
    """Generator for Model Three attestation certificates (date-specific variant).

    Creates attestation documents confirming residency with specific date
    requirements (30+ days residency, or specific effective dates for certain
    certificate types).

    Attributes:
        data (DocumentData): Certificate context with person records and type data.
        text (str): Generated certificate body text in Portuguese.
    """

    def __init__(self, data: DocumentData):
        """Initialize date-specific attestation document generator.

        Args:
            data (DocumentData): Container with person, certificate type, and form data.
        """
        self.data = data
        self.text = ""

    def create_text(self):
        """Generate date-specific certificate text and render to PDF.

        Constructs certificate body confirming residency with date requirements.
        Different time periods based on certificate type:
        - Study grants: 3+ years residency
        - Default: 30+ days residency
        - Type ID 8: Specific effective date from form data

        Returns:
            tuple: (text, pdf_url, success_bool) where text is the certificate body,
                   pdf_url is the storage URL, and success_bool indicates PDF generation success.
        """
        fim = "Efeitos de "
        tempo = " há mais de trinta dias e nos últimos doze meses"
        data = self.data

        if data.type2.name == "Bolsa de Estudo":
            tempo = " há mais de três anos e nos últimos doze meses"
            fim = "Efeitos de "
        elif data.type2.id == 8:
            tempo = f", desde {StringHelper.ext_data(StringHelper,data.data['date'])}"

        self.text = f"Atesta para {fim} {data.type2.name} que, {StringHelper.text_bi(StringHelper, data.type2,data.bi1,data.bi2,data.data)} reside efetivamente {StringHelper.house_address(StringHelper, data.bi1.address)}, deste Estado{tempo}."

        pdf_object = PDF(self.text, self.data.type, self.data.type2, data.certificate, self.data.data, self.data.bi1)
        file_name, status = pdf_object.render_pdf()
        return self.text, file_name, status

        # //text, type1,AtestadoTypes type2, Gerados gerado, DocumentForm form = null, Bis bi = null
