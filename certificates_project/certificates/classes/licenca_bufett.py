from certificates.models import CertificateDate, CertificateSinglePerson
from .pdf import PDF
from .string_helper import StringHelper
from certificates.classes.interfaces.document import Document
from pprint import pprint
from .document_data import DocumentData


class LicencaBufett(Document):
    def __init__(self, data: DocumentData):
        self.data = data
        self.text = ""

    def create_text(self):
        data = self.data

        # user
        simple_days = CertificateDate.objects.optimized().filter(type_id=data.type2.id)

        simple_days_text = StringHelper.ext_days(
            StringHelper, simple_days.order_by("date__year", "date__month", "date__day"))

        final = ""
        if data.type2.id in [ 29]:
            final = f"para que nos termos da Legislação Vigente, passa a explorar {simple_days_text}{StringHelper.street_address(StringHelper, data.data['street'])}, {data.data['infra']}"
        elif data.type2.id == 32:
            final = f", deste Estado para proceder {data.data['infra']} {StringHelper.street_address(StringHelper, data.data['street'])}, de {StringHelper.NumeroEmExtenso(data.data['metros'])} metros quarados{simple_days_text[:-2]}"

        self.text = f"Por esta Câmara se faz Constar as autoridades e mais pessoas a quem o conhecimento desta competir que foi concedida a  Licença {StringHelper.oa4(StringHelper,data.bi1.gender)} senhor{StringHelper.oa2(StringHelper,data.bi1.gender)}{StringHelper.text_bi(StringHelper, data.type2,data.bi1,data.bi2,data.data)} residente em {StringHelper.house_address(StringHelper, data.bi1.address)} {final}."

        pdf_object = PDF(self.text, self.data.type, self.data.type2,
                         data.certificate, self.data.data, self.data.bi1)
        file_name, status = pdf_object.render_pdf()
        return self.text, file_name, status

        # return new PDF($this->text,$this->getType(),$this->getType2(), $this->getGerados(), $this->getForm());
