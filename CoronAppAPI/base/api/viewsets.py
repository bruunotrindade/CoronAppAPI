from rest_framework import response, status, viewsets, permissions, mixins
from rest_framework.decorators import api_view
from django.db.models import Count, Q, Sum, F

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


class RecommendationViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request,  *args, **kwargs):
        try:
            app_user = AppUser.objects.get(id=self.kwargs['pk'])
        except AppUser.DoesNotExist:
            return response.Response('Usuario nao encontrado', status=status.HTTP_404_NOT_FOUND)

        symptoms_actives = SymptomOccurrence.objects.filter(
            user__id=self.kwargs['pk'], end_date__isnull=True
        ).prefetch_related('symptom')
        diseases_actives = Disease.objects.filter(userapp_set__id=self.kwargs['pk'])
        characteristics_actives = Characteristic.objects.filter(userapp_set__id=self.kwargs['pk'])
        common = critical = exterior = grupo_risco = contato_infectado = aglomeracao = False
        recommendation = []
        if diseases_actives or app_user.yearsOld() >= 60:
            grupo_risco = True
        if characteristics_actives:
            for char in characteristics_actives:
                if char.name.lower() in ['infectado']:
                    contato_infectado = True
                elif char.name.lower() in ['exterior']:
                    exterior = True
                elif char.name.lower() in ['aglomeracao']:
                    aglomeracao = True

        for occurrence in symptoms_actives:
            if occurrence.symptom.type_symptom == Symptom.COMMON:
                common = True
            elif occurrence.symptom.type_symptom == Symptom.CRITICAL:
                critical = True
            else:
                pass

        if grupo_risco or contato_infectado or common or exterior or aglomeracao:
            recommendation.append('isolamento')
        if (common and critical) or \
                (contato_infectado and grupo_risco) or \
                (grupo_risco and critical) or \
                (grupo_risco and critical and common):
            recommendation.append('atendimento')

        return response.Response({'recommendation': recommendation}, status=status.HTTP_200_OK)


@api_view(['GET'])
def all_datas(request):
    data = {
        'diseases': [{'id': disease.id, 'name': disease.name} for disease in Disease.objects.all()],
        'symptoms': [
            {
                'id': symptom.id,
                'name': symptom.name,
                'type_symptom': symptom.type_symptom
            } for symptom in Symptom.objects.all()
        ],
        'chars': [{'id': char.id, 'name': char.name} for char in Characteristic.objects.all()]}

    return response.Response(data, status=status.HTTP_200_OK)
