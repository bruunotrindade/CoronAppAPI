from rest_framework import serializers

from base.models import Disease, Symptom, Characteristic, AppUser, Temperature, SymptomOccurrence


class DiseaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disease
        fields = ('name', )


class SymptomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Symptom
        fields = ('name', )


class CharacteristicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Characteristic
        fields = ('name', 'question')


class AppUserSerializer(serializers.ModelSerializer):
    chars = CharacteristicSerializer(many=True)
    diseases = DiseaseSerializer(many=True)
    symptoms = SymptomSerializer(many=True)

    class Meta:
        model = AppUser
        fields = ('email', 'dob', 'state', 'city', 'chars', 'diseases', 'symptoms')


class TemperatureSerializer(serializers.ModelSerializer):
    user = AppUserSerializer()

    class Meta:
        model = Temperature
        fields = ('value', 'date', 'user')


class SymptomOccurrenceSerializer(serializers.ModelSerializer):
    symptom = SymptomSerializer()
    user = AppUserSerializer()

    class Meta:
        model = SymptomOccurrence
        fields = ('date', 'symptom', 'status', 'user')





