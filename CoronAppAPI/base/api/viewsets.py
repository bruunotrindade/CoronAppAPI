from rest_framework import response, status, viewsets, permissions, mixins
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, Sum, F

from base.api.serializers import (
    DiseaseSerializer, SymptomSerializer, AppUserSerializer, CharacteristicSerializer, SymptomOccurrenceSerializer,
    TemperatureSerializer, SymptomOccurrenceCreateSerializer
)
from base.models import Disease, Symptom, Characteristic, AppUser, Temperature, SymptomOccurrence
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


class LastTemperatureViewset(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = TemperatureSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            app_user = AppUser.objects.get(id=self.kwargs['pk'])
        except AppUser.DoesNotExist:
            return response.Response('Usuario nao encontrado', status=status.HTTP_404_NOT_FOUND)

        queryset = Temperature.objects.filter(user=app_user).last()
        serializer = self.get_serializer(queryset)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


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


class SymptomOccurrenceCreateViewset(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = SymptomOccurrenceCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = serializer.fields['idUser'].queryset[0]
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = SymptomOccurrence.objects.filter(user=user, end_date__isnull=True)
        instance_serializer = SymptomOccurrenceSerializer(instance, many=True)
        return response.Response(instance_serializer.data, status=status.HTTP_201_CREATED)


class RecommendationViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]

    '''def get_queryset(self):
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

        q1 = Recommendation.objects.filter()'''
        
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
            if occurrence.symptom:
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
        if len(recommendation) == 0:
            recommendation.append('fica em casa')

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
        'chars': [{'id': char.id, 'name': char.name, 'question': char.question} for char in Characteristic.objects.all()]}

    return response.Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def verify_email(request, email):
    user = get_object_or_404(AppUser, email=email) 
    data_user = AppUserSerializer(user)

    token = gerar_token()

    message = 'Bem Vindo ao CovidApp! \n Para validar o seu email, digite o código abaixo em seu aplicativo: \n Código: ' +  token + '\n' 
    send_mail('CovidApp - Confirmação de Email', message, 'covidappbr@gmail.com', [email])

    return response.Response({'User': data_user.data, 'Token': token}, status=status.HTTP_200_OK)

