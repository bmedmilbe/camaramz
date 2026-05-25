from certificates.models import CertificateSinglePerson
from .pdf import PDF
from .string_helper import StringHelper
from certificates.classes.interfaces.document import Document
from pprint import pprint
from .document_data import DocumentData


class LicencaTransladacao(Document):
    def __init__(self,data: DocumentData):
        self.data = data
        self.text = ""

    def create_text(self):
        data = self.data
    
        self.text = f"Por esta Câmara se faz Constar as autoridades e mais pessoas a quem o conhecimento desta competir que foi concedida Autorização {StringHelper.oa4(StringHelper,data.bi1.gender)} senhor{StringHelper.oa2(StringHelper,data.bi1.gender)}{StringHelper.text_bi(StringHelper, data.type2,data.bi1,data.bi2,data.data)} residente em {StringHelper.house_address(StringHelper, data.bi1.address)} para proceder a transladação da ossada d{StringHelper.oa(StringHelper,data.data['coval'].gender)} {data.data['coval'].name}, falecid{StringHelper.oa(StringHelper,data.data['coval'].gender)} em {StringHelper.ext_data(StringHelper,data.data['coval'].date_of_deth)} e Sepultad{StringHelper.oa(StringHelper,data.data['coval'].gender)} em {StringHelper.ext_data(StringHelper,data.data['coval'].date_used)} no Cemitério de {data.data['coval'].cemiterio.name}."
        

        pdf_object = PDF(self.text,self.data.type,self.data.type2, data.certificate, self.data.data,self.data.bi1)
        file_name, status = pdf_object.render_pdf()
        return self.text, file_name, status

        # return new PDF($this->text,$this->getType(),$this->getType2(), $this->getGerados(), $this->getForm());
    