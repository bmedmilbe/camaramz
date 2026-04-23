
from decimal import Decimal
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.files.storage import default_storage
from certificates.classes.string_helper import StringHelper
from certificates.models import Certificate, CertificateTitle, CertificateTypes, Ifen, Person
from datetime import date, timedelta
from io import BytesIO
from django.core.files.base import ContentFile


class PDF():
    def __init__(self, text, type1: CertificateTypes, type2: CertificateTitle, gerado: Certificate, form, bi: Person):
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
        ifen = Ifen.objects.get(name="data")
        dash = ifen.size * " -"

        self.date = f"- - - Câmara Distrital de {self.bi.address.street.town.county.name}, na Cidade da Trindade, aos {self.date}."

        self.date = f"{self.date}{dash[len(self.date):]}"

        ifen = Ifen.objects.get(name="texto")
        resto = len(self.text) % 88
        dash = int((resto + (88 - resto))) * "-"

        self.text = f"{self.text}"

        template = get_template("certificates/certificate_off.html")

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

        # 2. Define your paths (S3 likes forward slashes)
        # This path is relative to your MEDIA_ROOT or S3 Bucket root
        folder_name = f"certificates/{self.type2.id}-{self.type1.slug}-de-{self.type2.slug[10:]}"
        file_name = f"{self.certificate.number}.pdf"
        full_path = f"{folder_name}/{file_name}"

        # 3. Save to Storage (S3 or Local)
        # default_storage.save() automatically handles directory creation
        pdf_content = ContentFile(pdf_buffer.getvalue())

        # Optional: Delete if it already exists to mimic your "shutil.rmtree" logic
        if default_storage.exists(full_path):
            default_storage.delete(full_path)

        # 4. Update the Model
        # We pass the ContentFile directly to the model field
        certificate = Certificate.objects.get(id=self.certificate.id)

        certificate.file.save(full_path, pdf_content)

        return certificate.file.url, True

    def conta(self, type1: CertificateTypes, type2: CertificateTitle, atestado_number, autoV=0, cplp=False):

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
            rest = 5 * " -"
            size = 62 * " -"
            temp_text = f"- - - Válida até {StringHelper.ext_data(StringHelper,expire_date)}."
            text = f"""{text}
            {temp_text}{size[len(temp_text):]}
            - - - Às autoridades e mais a quem o conhecimento desta competir assim o tenham entendido.{rest[1:]}"""

        return text
