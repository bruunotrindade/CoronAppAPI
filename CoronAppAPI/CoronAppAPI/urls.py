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
from django.urls import path
from rest_framework import routers

from base.api.viewsets import (
    AppUserViewset, CharacteristicViewset, DiseaseViewset, SymptomOccurrenceViewset, SymptomViewset, TemperatureViewset
)


router = routers.DefaultRouter()
router.register(r'disease', DiseaseViewset, basename='DiseaseApp')
router.register(r'appuser', AppUserViewset, basename='UserApp')
router.register(r'characteristic', CharacteristicViewset, basename='CharacteristicApp')
router.register(r'symptom', SymptomViewset, basename='SymptomApp')
router.register(r'temperature', TemperatureViewset, basename='TemperatureApp')
router.register(r'symptomoccurrence', SymptomOccurrenceViewset, basename='SymptomOccurrenceApp')

urlpatterns = [
    path('admin/', admin.site.urls),
]
