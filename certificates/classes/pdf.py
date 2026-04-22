"""PDF generation and management for certificates.

This module handles the generation, rendering, and storage of PDF certificates
using xhtml2pdf (pisa). Manages certificate text formatting, pricing calculations,
and file storage to both local and S3 cloud storage.

Classes:
    PDF: Main class for certificate PDF generation and storage.
"""

from decimal import Decimal
from io import BytesIO
import os
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.files import File
import uuid
from django.conf import settings
from django.core.files.storage import default_storage
from certificates.classes.string_helper import StringHelper
from certificates.models import Certificate, CertificateDate, CertificateTitle, CertificateTypes, Ifen, Person
from datetime import date, timedelta
from django.core.files.base import ContentFile
from pprint import pprint


class PDF():
    """Generates and manages PDF certificates with pricing and formatting.

    Handles the complete PDF generation workflow including text formatting,
    price calculations, template rendering, and file storage to cloud (S3)
    or local storage. Supports multiple certificate types with different
    pricing and layout rules.

    Attributes:
        text (str): The main certificate body text content.
        type1 (CertificateTypes): The certificate type classification.
        type2 (CertificateTitle): The specific certificate title/variant.
        certificate (Certificate): The certificate model instance being generated.
        data (dict): Form data containing certificate-specific information.
        bi (Person): The person (individual) the certificate is for.
        presidente (str): Name of the district president/official.
        distrito (str): The administrative district name.
        date (str): Formatted issue date string.
        footer (str): Footer text with formatted date.
        final_text (str): Final formatted text for the certificate body.
        conta_details (dict): Pricing breakdown (total, fees, taxes).
    """

    def __init__(self, text, type1: CertificateTypes, type2: CertificateTitle, gerado: Certificate, form, bi: Person):
        """Initialize PDF generator with certificate data.

        Args:
            text (str): Main certificate body text content.
            type1 (CertificateTypes): Certificate type classification.
            type2 (CertificateTitle): Specific certificate title/variant.
            gerado (Certificate): Generated certificate model instance.
            form (dict): Form data dictionary with certificate-specific fields.
            bi (Person): Person (individual) the certificate is for.
        """
        self.pdf_root = ""
        self.pdf_name = ""
        self.pdf_number = ""

        self.text = text
        self.type1 = type1
        self.type2 = type2
        self.certificate = gerado
        self.data = form
        self.bi = bi
        self.presidente = "ANAHORY DIAS ABÍLIO DO ESPÍRITO"
        self.distrito = "MÉ-ZÓCHI"
        self.date = StringHelper.ext_data(StringHelper, gerado.date_issue)

        self.footer = StringHelper.data(StringHelper, gerado.date_issue)

        self.final_text = self.textoFinal(
            self.type1, self.data.get('last_date'))

        value = type2.type_price
        if type2.id == 8 and self.bi.birth_address.id in [3, 4, 7, 8, 9, 12, 13, 14, 15]:
            self.conta_details = self.conta(
                type1, type2, gerado.number, 1847.5, True)

        elif type2.id == 8:
            self.conta_details = self.conta(
                type1, type2, gerado.number, 2460, True)

        elif type2.id == 25:
            self.conta_details = self.conta(
                type1, type2, gerado.number, self.data['change'].price)

        elif type2.id == 27:

            self.conta_details = self.conta(
                type1, type2, gerado.number, self.data['range'].price)

        elif type2.id in [29, 32]:
            if not self.data['metros']:  # metros none
                value = 250 * self.data['dates'].count()
            else:
                if self.data['metros'] >= 4:
                    value = 175 * self.data['dates'].count()
                else:
                    value = 175 * self.data['dates'].count() + (
                        int(self.data['metros']) - 4) * 50 * self.data['dates'].count()

                value = (value) + 10

            self.conta_details = self.conta(type1, type2, gerado.number, value)
        elif type2.id == 31:

            value = type2.type_price + 10

            self.conta_details = self.conta(type1, type2, gerado.number, value)
        else:
            self.conta_details = self.conta(type1, type2, gerado.number, value)

    def render_pdf(self):
        """Render certificate HTML template to PDF and save to storage.

        Performs the following steps:
        1. Fetches IFEN (formatting) settings from database
        2. Formats date and text with appropriate dashes/padding
        3. Renders Django template with certificate data
        4. Converts HTML to PDF using xhtml2pdf (pisa)
        5. Saves PDF file to S3 or local storage
        6. Updates Certificate model with file path

        Returns:
            tuple: (pdf_url, success_bool) where pdf_url is the file URL or empty string
                   and success_bool indicates if generation succeeded.

        Raises:
            Certificate.DoesNotExist: If certificate record is not found during save.
        """
        ifen = Ifen.objects.get(name="data")
        dash = ifen.size * " -"

        self.date = f"- - - Câmara Distrital de {self.bi.address.street.town.county.name}, na Cidade da Trindade, aos {self.date}."

        self.date = f"{self.date}{dash[len(self.date):]}"

        ifen = Ifen.objects.get(name="texto")
        resto = len(self.text) % 88
        dash = int((resto + (88 - resto))) * "-"
        self.text = f"{self.text}"

        template = get_template("certificates/certificate_off.html")

        context = {}
        context_dict = {
            'body': self.text,
            'presidente': f"{self.presidente}",
            'distrito': f"{self.bi.address.street.town.county.name.upper()}",
            'town': f"{self.bi.address.street.town.name}",
            'certificate': self.certificate,
            'type1': self.type1,
            'type2': self.type2,
            'final_text': self.final_text,
            'date': self.date,
            'data': self.data,
            'prices': self.conta_details,
            'bi': self.bi,
            'logo': 'https://bm-edmilbe-bucket.s3.eu-north-1.amazonaws.com/camaramz/extras/stp.41e0f117.png'
        }

        # 1. Render HTML to PDF in memory
        html = template.render(context_dict)
        pdf_buffer = BytesIO()
        pisa_status = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf_buffer)

        if pisa_status.err:
            return '', False

        # 2. Define paths (S3 compatible format with forward slashes)
        folder_name = f"certificates/{self.type2.id}-{self.type1.slug}-de-{self.type2.slug[10:]}"
        file_name = f"{self.certificate.number}.pdf"
        full_path = f"{folder_name}/{file_name}"

        # 3. Save to Storage (S3 or Local)
        pdf_content = ContentFile(pdf_buffer.getvalue())

        if default_storage.exists(full_path):
            default_storage.delete(full_path)

        # 4. Update the Model
        certificate = Certificate.objects.get(id=self.certificate.id)
        certificate.file.save(full_path, pdf_content)

        return certificate.file.url, True

    def conta(self, type1: CertificateTypes, type2: CertificateTitle, atestado_number, autoV=0, cplp=False):
        """Calculate and break down certificate pricing (fees, taxes, etc).

        Calculates the total cost for a certificate based on its type and
        administrative location. Breaks down costs into:
        - Rasa (administrative processing fee)
        - Selo (stamp/seal fee)
        - Imposto (tax at 10% of adjusted value)
        - Emolumento (professional service fee)

        Args:
            type1 (CertificateTypes): Certificate type classification.
            type2 (CertificateTitle): Specific certificate title/variant.
            atestado_number (str): Certificate number for reference.
            autoV (int, optional): Override value for automatic calculation. Defaults to 0.
            cplp (bool, optional): Flag for CPLP (Portuguese-speaking) countries. Defaults to False.

        Returns:
            dict: Pricing breakdown with keys:
                - 'total': Total cost in currency units
                - 'rasa': Processing fee amount
                - 'selo': Stamp fee amount
                - 'emolumento': Professional service fee
                - 'imposto': Tax amount (10%)
                - 'total_extenso': Total cost written in words (Portuguese)
        """
        value = type2.type_price

        Total = 0
        Rasa = 10
        if type2.id == 33:
            value = type2.type_price
            Total = value
            value = value

        elif type2.id in [25, 29] or type2.id == 8 and cplp == True:
            Rasa = 100
            value = autoV
            Total = Total + Rasa
        elif type2.id == 27:
            value = autoV
            Total = Rasa = 5
        elif type2.id == 32:
            value = autoV
            Total = Rasa + 20
        else:
            Rasa = 5
            Total = Total + Rasa

        Selo = 10
        Total = Total + Selo
        Imposto = (value - (10)) * Decimal(0.1)
        Total = Total + Imposto
        Emolumento = (value - 10) - Rasa - Imposto
        Total = Total + Emolumento

        Zero = Emolumento + Rasa
        Rasa = 0 if Zero == 0 else Rasa
        Emolumento = 0 if Zero == 0 else Emolumento
        Emolumento = round(Emolumento, 2)
        Rasa = round(Rasa, 2)
        Selo = round(Selo, 2)
        Imposto = round(Imposto, 2)

        Total = round(Total, 2)

        return {
            'total': Total,
            'rasa': Rasa,
            'selo': Selo,
            'emolumento': Emolumento,
            'imposto': Imposto,
            'total_extenso': StringHelper.NumeroEmExtenso(Total)
        }

    def setTracoCenter(self, ct, string):

        c = int((ct - len(string)) / 2)

        newString = ""

        for i in range(0, c + 1):
            newString = f"{newString}-"

        newString = f"{newString}{string}"

    def setTracoData():
        return f"{Ifen.objects.get(name='DATA')}"

    def setTracoValidade():
        return f"{Ifen.objects.get(name='VALIDADE')}"

    def setTracoLast(self, ct, string):
        c = int((ct - len(string)))
        newString = f"------{string}"
        for i in range(0, c):
            newString = f"{newString}-"

        return newString

    def textoFinal(self, type1: CertificateTypes, expire_date=None):
        text_ifen = 109 * " -"
        text = f"""
        - - - Por ser verdade e ter sido requerido, mandou passar {type1.gender} presente {type1.name}, que assina, sendo a sua assinatura autenticada com o carimbo em uso nesta Câmara."""
        text = text + text_ifen[len(text):]

        if type1.id in [3, 4, 7]:
            text = ""
        elif type1.id == 6:
            startdate = date.today()
            enddate = startdate + timedelta(days=365)  # five years ago
            validade = StringHelper.ext_data(StringHelper, enddate)
            text = f"""{text}
            - - - Válida até {validade}"""
        elif type1.id == 8:
            # pprint("Aqui")
            # pprint(StringHelper.ext_data(StringHelper,expire_date))
            rest = 5 * " -"
            size = 62 * " -"
            temp_text = f"- - - Válida até {StringHelper.ext_data(StringHelper,expire_date)}."
            text = f"""{text}
            {temp_text}{size[len(temp_text):]}
            - - - Às autoridades e mais a quem o conhecimento desta competir assim o tenham entendido.{rest[1:]}"""

        return text

    def data(timestamp_date):
        startdate = date.today()
        data = StringHelper.DataEmExtenso(
            startdate.day, startdate.month, startdate.year)
        string = f"------Câmara Distrital de Mé-Zóchi, na Cidade da Trindade, aos {data}.{self.setTracoData()}"

        return string
