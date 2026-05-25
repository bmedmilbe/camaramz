from certificates.models import CertificateSinglePerson
from .pdf import PDF
from .string_helper import StringHelper
from certificates.classes.interfaces.document import Document
from .document_data import DocumentData


class AutoEnterro(Document):
    def __init__(self, data: DocumentData):
        self.data = data
        self.text = ""

    def create_text(self):
        data = self.data
        single_person = CertificateSinglePerson.objects.filter(type_id=data.type2.id).first()
        single_person_text = f"d{StringHelper.oa(StringHelper,single_person.gender)} {StringHelper.toBold(single_person.name)},"

        self.text = f"Autorizo o enterro {single_person_text} " \
                    f"no coval número {data.data['coval'].number}, " \
                    f"antigo {data.data['last_coval'].number}, " \
                    f"do Cemitério de {data.data['cemiterio'].name}, " \
                    f"falecid{StringHelper.oa(StringHelper,single_person.gender)} em {StringHelper.ext_data(StringHelper,data.data['died_date'])} e " \
                    f"Sepultad{StringHelper.oa(StringHelper,single_person.gender)} em {StringHelper.ext_data(StringHelper,data.data['entero_date'])}, ao " \
                    f"pedido d{StringHelper.oa(StringHelper,data.bi1.gender)}{StringHelper.text_bi(StringHelper, data.type2,data.bi1,data.bi2,data.data)} residente " \
                    f"em {StringHelper.house_address(StringHelper, data.bi1.address)}."

        pdf_object = PDF(self.text, self.data.type, self.data.type2, data.certificate, self.data.data, self.data.bi1)
        file_name, status = pdf_object.render_pdf()
        return self.text, file_name, status
