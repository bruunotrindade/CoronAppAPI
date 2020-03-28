from rest_framework import response, status, viewsets, permissions
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from base.api.serializers import (
    DiseaseSerializer, SymptomSerializer, AppUserSerializer, CharacteristicSerializer, SymptomOccurrenceSerializer,
    TemperatureSerializer, RecommendationSerializer
)
from base.models import Disease, Symptom, Characteristic, AppUser, Temperature, SymptomOccurrence, Recommendation
from .utils import gerar_token

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
        user = AppUser.objects.get(pk=self.kwargs['pk'])
        symptoms_user = SymptomOccurrence.objects.filter(user=user, end_date__isnull=True)
        diseases_user = user.diseases
        chars_user = user.chars

        recommendations = Recommendation.objects.all()

        # Filtra as recomendações com os mesmos sintomas
        rec1 = [ rec for rec in recommendations 
                  if all( sym in rec['symptoms'] 
                  for sym in symptoms_user ) 
        ]

        # Filtra as recomendações com as mesmas doenças
        rec2 = [ rec for rec in rec1 
                  if all( dis in rec['diseases'] 
                  for dis in diseases_user ) 
        ]

        # Filtra as recomendações com as mesmas caracteristicas
        rec3 = [ rec for rec in rec2 
                  if all( char in rec['characteristics'] 
                  for char in chars_user ) 
        ]

        # Recomendações que sobraram
        print(rec3)

        # occurrences_user = SymptomOccurrence.objects.filter(user=self.kwargs['pk'])
        # for occurrence in occurrences_user:
        #     if occurrence.status == SymptomOccurrence.BEGIN and \
        #             not occurrences_user.filter(symptom=occurrence.symptom, status=SymptomOccurrence.END):
        #         occurrences_actives.append(occurrence)

        q1 = Recommendation.objects.filter()


@api_view(['GET'])
def all_datas(request):
    data = {}

    data['diseases'] = [{'id': disease.id, 'name': disease.name} for disease in Disease.objects.all()]
    data['symptoms'] = [{'id': symptom.id, 'name': symptom.name, 'type_symptom': symptom.type_symptom} for symptom in Symptom.objects.all()]
    data['chars']    = [{'id': char.id, 'name': char.name} for char in Characteristic.objects.all()]

    return response.Response(data)

@api_view(['GET'])
def verify_email(request, email):
    user = get_object_or_404(AppUser, email=email) 
    data_user = AppUserSerializer(user)

    token = gerar_token()

    message = 'Bem Vindo ao CovidApp! \n Para validar o seu email, digite o código abaixo em seu aplicativo: \n Código: ' +  token + '\n' 
    send_mail('CovidApp - Confirmação de Email', message, 'covidappbr@gmail.com', [email])

    return response.Response({'User': data_user.data, 'Token': token}, status=status.HTTP_200_OK)

