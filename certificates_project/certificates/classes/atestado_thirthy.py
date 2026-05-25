from .pdf import PDF
from .string_helper import StringHelper

class AtestadoThirthy(DocumentData, Document):
    
    def create(self):


        fim = "Efeitos de "


        tempo = " há mais de trinta dias e nos últimos doze meses"



        if self.type2.name == "Bolsa de Estudo":
            tempo = " há mais de três anos e nos últimos doze meses"
            fim = "Efeitos de "
        if self.type2.name == 8:
            tempo = ", desde " . self.form.getNasDate.getExtData        

        self.text = f"Atesta para  {fim} {self.type2.name} que, {StringHelper.getTextBi(self.bi1, self.bi2,self.type2.id)} reside efetivamente  {self.form.house_txt}  na localidade de {self.form.localidade.name}, Distrito de Mé-Zochi, deste Estado{tempo}."

        pdf_object = PDF(self.text,self.data.type,self.data.type2, data.certificate, self.data.data,self.data.bi1)
        file_name, status = pdf_object.render_pdf()
        return self.text, file_name, status