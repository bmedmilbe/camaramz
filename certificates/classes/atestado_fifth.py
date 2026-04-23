from certificates.models import CertificateSimplePerson, CertificateSinglePerson
from .pdf import PDF
from .string_helper import StringHelper
from certificates.classes.interfaces.document import Document
from .document_data import DocumentData


class AtestadoFifth(Document):
    def __init__(self, data: DocumentData):
        self.data = data
        self.text = ""

    def create_text(self):

        fim = "Fins de "
        data = self.data
        text = ""
        simple_persons = []
        single_person = None
        single_person_text = ""
        if data.type2.id == 12:
            simple_persons = CertificateSimplePerson.objects.filter(type_id=data.type2.id)
            text = StringHelper.simple_person_text(StringHelper, simple_persons)

            single_person = CertificateSinglePerson.objects.filter(type_id=data.type2.id).first()

            single_person_text = f"d{StringHelper.oa(StringHelper,single_person.gender)} {StringHelper.toBold(single_person.name)}, que  foi funcionári{StringHelper.oa(StringHelper,single_person.gender)} de {data.data['instituition'].name}"

        qtd = simple_persons.count()

        m = "m" if qtd > 1 else ""

        oa_22 = "o"
        if qtd == 1 and simple_persons.first().gender == "F":
            oa_22 = "a"
        elif qtd > 1:
            oa_22 = "as"
            for person in simple_persons:
                if person.gender == "M":
                    oa_22 = "os"

        if data.type2.id == 12:
            self.text = f"Atesta para {fim} {data.type2.name} {single_person_text}, a favor de {StringHelper.text_bi(StringHelper, data.type2,data.bi1,data.bi2,data.data)} residente {StringHelper.house_address(StringHelper, data.bi1.address)}, deste Estado, destinada a subsistência{text}atesta-se ainda que {oa_22} mesm{oa_22} dependia{m} financeiramente d{StringHelper.oa(StringHelper,single_person.gender)} falecid{StringHelper.oa(StringHelper,single_person.gender)}."

        pdf_object = PDF(self.text, self.data.type, self.data.type2, data.certificate, self.data.data, self.data.bi1)
        file_name, status = pdf_object.render_pdf()
        return self.text, file_name, status
