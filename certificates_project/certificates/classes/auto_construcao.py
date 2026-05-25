from certificates.models import CertificateSinglePerson
from .pdf import PDF
from .string_helper import StringHelper
from certificates.classes.interfaces.document import Document
from pprint import pprint
from .document_data import DocumentData


class AutoConstrucao(Document):
    def __init__(self, data: DocumentData):
        self.data = data
        self.text = ""

    def create_text(self):
        data = self.data

        tempo = ""

    #     self.text = "Por esta Câmara se faz constar as autoridades e mais pessoas a quem o
    #  conhecimento desta competir que foi concedida Autorização " .
    #         $this->getBi1()->getBiOa3() . " senhor" .$this->getBi1()->getBiOa2() . " " .
    #         StringHelper::getTextBi($this->getBi1(), $this->getBi2(),$this->getType2()->getTypeId(), $this->getForm())
    #         . "residente na " . $this->getForm()->getLocalidade()->getLocalidadeFull() .
    #         " para proceder a construção de " . $this->getForm()->getTipo()->getAutocreatetypeName() . "
    #  na localidade de ".  $this->getForm()->getLocalidade1()->getLocalidadeName().
    #         ", Distrito de Mé-Zóchi, São Tomé.";

        building_type = data.data['building_type']
        StringHelper.house_address(StringHelper, data.bi1.address)
        self.text = f"Por esta Câmara se faz constar as autoridades e mais pessoas a quem o conhecimento desta competir que foi concedida Autorização {StringHelper.oa4(StringHelper,data.bi1.gender)} senhor{StringHelper.oa2(StringHelper,data.bi1.gender)}{StringHelper.text_bi(StringHelper, data.type2,data.bi1,data.bi2,data.data)} residente {StringHelper.house_address(StringHelper, data.bi1.address)} para proceder a construção de {f'{building_type.prefix} ' if  building_type.prefix else ''}{building_type.name} {StringHelper.street_address(StringHelper, data.data['street'])}."

        pdf_object = PDF(self.text, self.data.type, self.data.type2,
                         data.certificate, self.data.data, self.data.bi1)
        file_name, status = pdf_object.render_pdf()
        return self.text, file_name, status

        # return new PDF($this->text,$this->getType(),$this->getType2(), $this->getGerados());
