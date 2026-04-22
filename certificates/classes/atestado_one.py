"""Certificate attestation (Atestado) generation for Model One documents.

This module implements the Model One certificate format - a simple attestation
document confirming residency and financial status for various administrative
purposes (study grants, poverty declarations, travel documentation, etc.).

Classes:
    AtestadoOne: Generator for Model One certificate documents.
"""

from .pdf import PDF
from .string_helper import StringHelper
from certificates.classes.interfaces.document import Document
from pprint import pprint
from .document_data import DocumentData


class AtestadoOne(Document):
    """Generator for Model One attestation certificates.

    Creates simple attestation documents (Atestado) confirming residency
    and financial/social status. Supports multiple purposes including:
    - Bolsa de Estudo (study grants) - requires 3+ years residency
    - Poverty declarations
    - Travel documentation to Portuguese Republic
    - General residency confirmation

    Attributes:
        data (DocumentData): Certificate context with person records and type data.
        text (str): Generated certificate body text in Portuguese.
    """

    def __init__(self, data: DocumentData):
        """Initialize attestation document generator.

        Args:
            data (DocumentData): Container with person, certificate type, and form data.
        """
        self.data = data
        self.text = ""

    def create_text(self):
        """Generate certificate text and render to PDF.

        Constructs the certificate body text based on certificate type and
        person data, then renders to PDF using the PDF class.

        Different text formats based on certificate title ID:
        - ID 11: Poverty declaration
        - ID 30: Poverty declaration (alternate format)
        - ID 34: Travel-related poverty declaration
        - Other (including "Bolsa de Estudo"): Residency + financial status

        Returns:
            tuple: (text, pdf_url, success_bool) where text is the certificate body,
                   pdf_url is the storage URL, and success_bool indicates PDF generation success.
        """
        fim = "Fins de "
        tempo = ""
        data = self.data

        if data.type2.name == "Bolsa de Estudo":
            tempo = " há mais de três anos e nos últimos doze meses"
            fim = "Efeitos de "

        if data.type2.id == 11:
            tempo = ", é pobre"

        if data.type2.id == 30:
            fim = "Fins "
            tempo = ", é pobre"

        if data.type2.id == 34:
            fim = "Fins "
            tempo = ", é pobre, não dispõe de meios para custear despesa com a sua viagem á República Portuguesa"

        self.text = f"Atesta para {fim} {data.type2.name} que, {StringHelper.text_bi(StringHelper, data.type2,data.bi1,data.bi2,data.data)} reside efetivamente {StringHelper.house_address(StringHelper, data.bi1.address)}, deste Estado{tempo}."

        pdf_object = PDF(self.text, self.data.type, self.data.type2, data.certificate, self.data.data, self.data.bi1)
        file_name, status = pdf_object.render_pdf()

        return self.text, file_name, status
