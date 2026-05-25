from .pdf import PDF
from .string_helper import StringHelper
from certificates.classes.interfaces.document import Document
from pprint import pprint
from .document_data import DocumentData


class AtestadoSecond(Document):
    def __init__(self, data: DocumentData):
        self.data = data
        self.text = ""

    def create_text(self):

        fim = "Fins de "
        tempo = ""
        data = self.data

        if data.type2.name == "Bolsa de Estudo":
            tempo = " há mais de três anos e nos últimos doze meses"
            fim = "Efeitos de "

        end = "." if data.type2.id == 13 else f" não dispõe de recursos para custear despesas com os seus estudos no(a) {data.data['university'].name} {tempo}."
        # self.text = f"Atesta para {fim} {self.type2.name}, á conceder pelo(a) {self.institution.name} que, {StringHelper.getTextBi(self.bi1, self.bi2,self.type2.id)} reside efetivamente {self.form.house_ext} na localidade de {self.form.localidade.name} Distrito de Mé-Zochi, deste Estado não dispõe de recursos para custear despesas com os seus estudos no(a) {self.form.university} {tempo}"

        self.text = f"Atesta para {fim} {data.type2.name}, á conceder pelo(a) {data.data['instituition'].name} que, {StringHelper.text_bi(StringHelper, data.type2,data.bi1,data.bi2,data.data)} reside efetivamente {StringHelper.house_address(StringHelper, data.bi1.address)}, deste Estado{end}"

        pdf_object = PDF(self.text, self.data.type, self.data.type2,
                         data.certificate, self.data.data, self.data.bi1)
        pprint(data.certificate.file)

        file_name, status = pdf_object.render_pdf()
        # pprint(pdf_object)
        return self.text, file_name, status
