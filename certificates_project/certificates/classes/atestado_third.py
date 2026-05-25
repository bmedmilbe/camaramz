from .pdf import PDF
from .string_helper import StringHelper
from certificates.classes.interfaces.document import Document
from pprint import pprint
from .document_data import DocumentData

class AtestadoThird(Document):
    def __init__(self,data: DocumentData):
        self.data = data
        self.text = ""

    def create_text(self):

        fim = "Efeitos de "
        tempo = " há mais de trinta dias e nos últimos doze meses"
        data = self.data

        if data.type2.name == "Bolsa de Estudo":
            tempo = " há mais de três anos e nos últimos doze meses"
            fim = "Efeitos de "
        elif data.type2.id == 8:
            tempo = f", desde {StringHelper.ext_data(StringHelper,data.data['date'])}"
        

        self.text = f"Atesta para {fim} {data.type2.name} que, {StringHelper.text_bi(StringHelper, data.type2,data.bi1,data.bi2,data.data)} reside efetivamente {StringHelper.house_address(StringHelper, data.bi1.address)}, deste Estado{tempo}."
        
        pdf_object = PDF(self.text,self.data.type,self.data.type2, data.certificate, self.data.data,self.data.bi1)
        file_name, status = pdf_object.render_pdf()
        return self.text, file_name, status

        # //text, type1,AtestadoTypes type2, Gerados gerado, DocumentForm form = null, Bis bi = null
    