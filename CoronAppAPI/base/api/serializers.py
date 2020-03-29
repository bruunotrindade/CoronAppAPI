from rest_framework import serializers

from base.models import (
    Disease, Symptom, Characteristic, AppUser, Temperature, SymptomOccurrence
)


class DiseaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disease
        fields = ('id', 'name', )


class SymptomSerializer(serializers.ModelSerializer):
    symptomType = serializers.CharField(source='get_type_symptom_display', read_only=True)

    class Meta:
        model = Symptom
        fields = ('id', 'name', 'symptomType')


# class UserSymptomSerializer(serializers.ModelSerializer):
#     id = serializers.ReadOnlyField(source='symptom.id')
#     name = serializers.ReadOnlyField(source='symptom.name')
#     type = serializers.ReadOnlyField(source='symptom.get_type_symptom_display')
#
#     class Meta:
#         model = UserSymptoms
#         fields = ('id', 'name', 'type', 'created_at')


class CharacteristicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Characteristic
        fields = ('id', 'name', 'question')


class SymptomOccurrenceListSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        symptoms = [SymptomOccurrence(**item) for item in validated_data]
        return SymptomOccurrence.objects.bulk_create(symptoms)


class SymptomOccurrenceSerializer(serializers.ModelSerializer):
    symptom = SymptomSerializer()

    class Meta:
        model = SymptomOccurrence
        list_serializer_class = SymptomOccurrenceListSerializer
        fields = ('id', 'start_date', 'end_date', 'symptom')


class AppUserSerializer(serializers.ModelSerializer):
    chars = CharacteristicSerializer(many=True, read_only=True)
    diseases = DiseaseSerializer(many=True, read_only=True)
    symptoms = SymptomOccurrenceSerializer(source='symptomoccurrence_set', many=True)
    setChars = serializers.PrimaryKeyRelatedField(
        source='chars', many=True, write_only=True, queryset=Characteristic.objects.all(), required=True,
    )
    setDiseases = serializers.PrimaryKeyRelatedField(
        source='diseases', many=True, write_only=True, queryset=Disease.objects.all(), required=True
    )
    setSymptoms = serializers.PrimaryKeyRelatedField(
        source='symptoms', many=True, write_only=True, queryset=Symptom.objects.all(), required=True
    )

    class Meta:
        model = AppUser
        fields = (
            'id', 'email', 'dob', 'state', 'city', 'chars', 'diseases', 'symptoms', 'setChars', 'setDiseases',
            'setSymptoms'
        )


class TemperatureSerializer(serializers.ModelSerializer):
    user = AppUserSerializer()

    class Meta:
        model = Temperature
        fields = ('id', 'value', 'date', 'user')






