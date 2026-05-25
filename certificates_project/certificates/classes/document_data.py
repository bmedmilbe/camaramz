from certificates.models import Person
from certificates.models import Certificate
from certificates.models import CertificateTypes
from certificates.models import CertificateTitle

class DocumentData():

    def __init__(self, 
                 bi:Person, 
                 validated_data,
                 certificate: Certificate,
                 bi2_id = None, 
                 certificate2 = None): #Certificate
    
        self.bi1 = bi
        self.bi2 = Person.objects.filter(id_number=bi2_id).first()
        self.type = CertificateTypes.objects.filter(id=certificate.type.certificate_type.id).first() 
        self.type2 = CertificateTitle.objects.filter(id=certificate.type.id).first()
        if certificate2:
            self.doc_update_number = certificate2.id
        
        self.data = validated_data
        self.certificate = certificate



       



    