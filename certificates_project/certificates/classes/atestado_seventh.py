
from certificates.models import CertificateSimpleParent, CertificateSinglePerson
from .pdf import PDF
from .string_helper import StringHelper
from certificates.classes.interfaces.document import Document
from pprint import pprint
from .document_data import DocumentData
class AtestadoSeventh(Document):
    def __init__(self,data: DocumentData):
        self.data = data
        self.text = ""

    def create_text(self):

        fim = "Fins de "
        data = self.data
       

        simple_parents = []
        tempo = f" há mais de {StringHelper.NumeroEmExtenso(data.data['years'])} ano{'s' if data.data['years'] > 1 else ''}."
        reside = "residente efetivamente"
        vive = "vive em comunhão de mesa e a"
       
        if data.data['country']:
            reside = "residiu"
            vive = f"atualmente á residir em {data.data['country'].name}, tem ao"
        
        
        simple_parents = CertificateSimpleParent.objects.filter(type_id=data.type2.id)
            # pprint(simple_persons)
        simple_parent_text = StringHelper.simple_parent_text(StringHelper,simple_parents.order_by('parent__gender'))
        
        
        self.text = f"Atesta para {fim} {data.type2.name} que {StringHelper.text_bi(StringHelper, data.type2,data.bi1,data.bi2,data.data)} {reside} {StringHelper.house_address(StringHelper, data.bi1.address)}, deste Estado, {vive} seu exclusivo cargo {simple_parent_text}{tempo}."
        
        
        pdf_object = PDF(self.text,self.data.type,self.data.type2, data.certificate, self.data.data,self.data.bi1)
        file_name, status = pdf_object.render_pdf()
        return self.text, file_name, status
    



