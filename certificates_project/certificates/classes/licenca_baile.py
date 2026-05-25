from certificates.models import CertificateDate, CertificateSinglePerson
from .pdf import PDF
from .string_helper import StringHelper
from certificates.classes.interfaces.document import Document
from pprint import pprint
from .document_data import DocumentData

class LicencaBaile(Document):
    def __init__(self,data: DocumentData):
        self.data = data
        self.text = ""

    def create_text(self):
        data = self.data
    

        simple_days = CertificateDate.objects.optimized().filter(type_id=data.type2.id)
        simple_days_text = StringHelper.ext_days(StringHelper,simple_days.order_by("date__year", "date__month", "date__day"))
        self.text = f"Por esta Câmara se faz Constar as autoridades e mais pessoas a quem o conhecimento desta competir que foi concedida a Licença {StringHelper.oa4(StringHelper,data.bi1.gender)} senhor{StringHelper.oa2(StringHelper,data.bi1.gender)}{StringHelper.text_bi(StringHelper, data.type2,data.bi1,data.bi2,data.data)} residente em {StringHelper.house_address(StringHelper, data.bi1.address)} para que nos termos da Legislação Vigente, passa a explorar {simple_days_text}{StringHelper.street_address(StringHelper, data.data['street'])}, {data.data['infra']}."
    
        pdf_object = PDF(self.text,self.data.type,self.data.type2, data.certificate, self.data.data,self.data.bi1)
        file_name, status = pdf_object.render_pdf()
        return self.text, file_name, status



        # $this->text = "


        # Por esta Câmara se faz as autoridades e mais
        # pessoas a quem o conhecimento desta competir que foi concedida
        # Licença " .  $this->getBi1()->getBiOa3() . " senhor" .$this->getBi1()->getBiOa2() . " " .
        #     StringHelper::getTextBi($this->getBi1(), $this->getBi2(),$this->getType2()->getTypeId(), $this->getForm())
        #     . "residente em " . $this->getForm()->getLocalidade()->getLocalidadeFull() . ", deste Estado para proceder
        #  ". $this->getForm()->getInfra() .
        #     ", na localidade de " .
        #     $this->getForm()->getLocalidade1()->getLocalidadeName()
        #     . ", " . $this->getForm()->getMetros(). " " . $this->getForm()->getData3() .".";

        # return new PDF($this->text,$this->getType(),$this->getType2(), $this->getGerados(), $this->getForm());
 