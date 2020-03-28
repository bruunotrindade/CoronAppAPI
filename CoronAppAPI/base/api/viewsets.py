from rest_framework import response, status, viewsets, permissions

from base.api.serializers import (
    DiseaseSerializer, SymptomSerializer, AppUserSerializer, CharacteristicSerializer, SymptomOccurrenceSerializer,
    TemperatureSerializer, RecommendationSerializer
)
from base.models import Disease, Symptom, Characteristic, AppUser, Temperature, SymptomOccurrence, Recommendation


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


class RecommendationViewset(viewsets.GenericViewSet):
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        occurrences_actives = SymptomOccurrence.objects.filter(user=self.kwargs['pk'], end_date__isnull=True)
        recommendations = Recommendation.objects.filter()

        # occurrences_user = SymptomOccurrence.objects.filter(user=self.kwargs['pk'])
        # for occurrence in occurrences_user:
        #     if occurrence.status == SymptomOccurrence.BEGIN and \
        #             not occurrences_user.filter(symptom=occurrence.symptom, status=SymptomOccurrence.END):
        #         occurrences_actives.append(occurrence)

        q1 = Recommendation.objects.filter()
