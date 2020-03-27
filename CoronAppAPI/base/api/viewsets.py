from rest_framework import response, status, viewsets, permissions
from rest_framework.decorators import api_view

from base.api.serializers import (
    DiseaseSerializer, SymptomSerializer, AppUserSerializer, CharacteristicSerializer, SymptomOccurrenceSerializer,
    TemperatureSerializer
)
from base.models import Disease, Symptom, Characteristic, AppUser, Temperature, SymptomOccurrence

class DiseaseViewset(viewsets.ModelViewSet):
    serializer_class = DiseaseSerializer
    queryset = Disease.objects.all()
    model = Disease
    permission_classes = [
        permissions.AllowAny
    ]


class SymptomViewset(viewsets.ModelViewSet):
    serializer_class = SymptomSerializer
    queryset = Symptom.objects.all()
    model = Symptom
    permission_classes = [
        permissions.AllowAny
    ]


class CharacteristicViewset(viewsets.ModelViewSet):
    serializer_class = CharacteristicSerializer
    queryset = Characteristic.objects.all()
    model = Characteristic
    permission_classes = [
        permissions.AllowAny
    ]


class TemperatureViewset(viewsets.ModelViewSet):
    serializer_class = TemperatureSerializer
    queryset = Temperature.objects.all()
    model = Temperature
    permission_classes = [
        permissions.AllowAny
    ]


class AppUserViewset(viewsets.ModelViewSet):
    serializer_class = AppUserSerializer
    queryset = AppUser.objects.all()
    model = AppUser
    permission_classes = [
        permissions.AllowAny
    ]


class SymptomOccurrenceViewset(viewsets.ModelViewSet):
    serializer_class = SymptomOccurrenceSerializer
    queryset = SymptomOccurrence.objects.all()
    model = SymptomOccurrence
    permission_classes = [
        permissions.AllowAny
    ]


@api_view(['GET'])
def all_datas(request):
    data = {}

    data['diseases'] = [disease for disease in Disease.objects.all()]
    data['chars']    = [char for char in Characteristic.objects.all()]
    data['symptoms'] = [symptom for symptom in Symptom.objects.all()]

    return response.Response(data)