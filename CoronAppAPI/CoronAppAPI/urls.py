"""CoronAppAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from base.api.viewsets import (
    AppUserViewset, CharacteristicViewset, DiseaseViewset, SymptomOccurrenceViewset, 
    SymptomViewset, RecommendationViewset, TemperatureViewset, all_datas, verify_email, SymptomOccurrenceCreateViewset,
    LastTemperatureViewset
)


router = routers.DefaultRouter()
router.register(r'diseases', DiseaseViewset, basename='DiseaseApp')
router.register(r'appusers', AppUserViewset, basename='UserApp')
router.register(r'characteristics', CharacteristicViewset, basename='CharacteristicApp')
router.register(r'symptoms', SymptomViewset, basename='SymptomApp')
router.register(r'temperatures', TemperatureViewset, basename='TemperatureApp')
router.register(r'symptomoccurrences', SymptomOccurrenceViewset, basename='SymptomOccurrenceApp')
router.register(r'addoccurrence', SymptomOccurrenceCreateViewset, basename='SymptomOccurrenceCreateApp')
router.register(r'recommendations', RecommendationViewset, basename='RecommendationApp')
router.register(r'last_temperature', LastTemperatureViewset, basename='LastTemperature')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/all_datas/', all_datas),
    path('api/email/<str:email>', verify_email)
]
