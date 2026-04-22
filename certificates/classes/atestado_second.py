"""Certificate attestation (Atestado) generation for Model Two documents.

This module implements the Model Two certificate format - an attestation
for institutional/educational purposes confirming residency and financial need
for study grants and similar programs.

Classes:
    AtestadoSecond: Generator for Model Two certificate documents.
"""

from .pdf import PDF
from .string_helper import StringHelper
from certificates.classes.interfaces.document import Document
from pprint import pprint
from .document_data import DocumentData


class AtestadoSecond(Document):
    """Generator for Model Two attestation certificates (institutional variant).

    Creates attestation documents confirming residency and inability to fund
    educational expenses. Commonly used for study grant (Bolsa de Estudo)
    applications.

    Attributes:
        data (DocumentData): Certificate context with person records and type data.
        text (str): Generated certificate body text in Portuguese.
    """

    def __init__(self, data: DocumentData):
        """Initialize institutional attestation document generator.

        Args:
            data (DocumentData): Container with person, certificate type, and form data.
        """
        self.data = data
        self.text = ""

    def create_text(self):
        """Generate institutional certificate text and render to PDF.

        Constructs certificate body confirming residency and financial need
        for institutional purposes (typically education). Includes institution
        name in the text.

        Different text formats based on certificate title ID:
        - ID 13: Simpler format without educational expense statement
        - Other: Full financial need statement for educational institution

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

        end = "." if data.type2.id == 13 else f" não dispõe de recursos para custear despesas com os seus estudos no(a) {data.data['university'].name} {tempo}."

        self.text = f"Atesta para {fim} {data.type2.name}, á conceder pelo(a) {data.data['instituition'].name} que, {StringHelper.text_bi(StringHelper, data.type2,data.bi1,data.bi2,data.data)} reside efetivamente {StringHelper.house_address(StringHelper, data.bi1.address)}, deste Estado{end}"

        pdf_object = PDF(self.text, self.data.type, self.data.type2,
                         data.certificate, self.data.data, self.data.bi1)

        file_name, status = pdf_object.render_pdf()

        return self.text, file_name, status
