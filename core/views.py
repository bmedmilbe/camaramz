
from rest_framework.views import APIView
from rest_framework.response import Response
from certificates.models import (
    Country, IDType, Instituition, Street, Town, County,
    University, Ifen, BiuldingType, Cemiterio, Change, CertificateTitle, Coval
)
from certificates.serializers import MetadataSerializer

from django.shortcuts import render


def api_home(request):
    """
    Renders the technical landing page for the Certificates API.
    """
    return render(request, 'api_home.html')


class UnifiedMetadataView(APIView):
    """
    Centralized metadata provider.
    Optimized with select_related to prevent N+1 query overhead.
    """

    def get(self, request):
        data = {
            "countries": Country.objects.all().order_by('name'),
            "universities": University.objects.all().order_by('name'),
            "ifens": Ifen.objects.all().order_by('name'),
            "buildings": BiuldingType.objects.all().order_by('name'),
            "cemiterios": Cemiterio.objects.all().order_by('name'),
            "streets": Street.objects.select_related('town').all().order_by('name'),
            "changes": Change.objects.all().order_by('name'),
            "towns": Town.objects.select_related('county').all().order_by('name'),
            "countys": County.objects.all().order_by('name'),
            "certificateTitles": CertificateTitle.objects.all().order_by('name'),
            "covals": Coval.objects.all().order_by('number'),
            "idtypes": IDType.objects.all().order_by('name'),
            "intituitions": Instituition.objects.all().order_by('name'),
        }
        serializer = MetadataSerializer(data)
        return Response(serializer.data)
