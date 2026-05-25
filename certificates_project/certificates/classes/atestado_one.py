from .pdf import PDF
from .string_helper import StringHelper
from certificates.classes.interfaces.document import Document
from pprint import pprint
from .document_data import DocumentData


class AtestadoOne(Document):
    def __init__(self, data: DocumentData):
        self.data = data
        self.text = ""

    def create_text(self):

        fim = "Fins de "
        tempo = ""
        data = self.data
        # pprint(self.data)
        # return {"data": f"{self.data}"}

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
        # pprint(data.certificate.file)

        file_name, status = pdf_object.render_pdf()
        return self.text, file_name, status

    # def pdf_render(self, ):
