from django.contrib import admin
from django import forms
from django.utils import timezone
from .models import *


class SymptomOccurrenceInline(admin.TabularInline):
    model = AppUser.symptoms.through


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    fieldsets = (
            ('Informações', {'fields': ('email', 'dob')}),
            ('Localização', {'fields': ('state', 'city')}),
            ('Geral', {'fields': ('chars', 'diseases')}),
        )

    inlines = [SymptomOccurrenceInline, ]

    list_display = ('email', 'dob', 'state', 'city')
    list_filter = ['state', 'city']
    search_fields = ('email', 'state', 'city')
    ordering = ('email', 'state', 'city')
    filter_horizontal = ()


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    fieldsets = (
            ('Descrição', {'fields': ('name',)}),
        )

    list_display = ('name',)
    filter_horizontal = ()


@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    fieldsets = (
            ('Descrição', {'fields': ('name', 'type_symptom')}),
        )

    list_display = ('name',)
    filter_horizontal = ()


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    fieldsets = (
            ('Descrição', {'fields': ('name', 'question')}),
        )

    list_display = ('name', 'question')
    filter_horizontal = ()


@admin.register(Temperature)
class TemperatureAdmin(admin.ModelAdmin):
    fieldsets = (
            ('Informações', {'fields': ('value', 'date', 'user')}),
        )

    list_display = ('user', 'value', 'date')
    filter_horizontal = ()


@admin.register(SymptomOccurrence)
class SymptomOccurrenceAdmin(admin.ModelAdmin):
    fieldsets = (
            ('Identificadores', {'fields': ('user', 'symptom')}),
            ('Descritivos', {'fields': ('start_date', 'end_date')}),
        )

    list_display = ('user', 'symptom', 'start_date', 'end_date')
    filter_horizontal = ()


admin.site.site_header = "CoronApp"
admin.site.index_title = "Gerenciamento"
admin.site.site_title = admin.site.site_header + " - Painel"
admin.site.site_url = None


