from rest_framework import serializers

from base.models import Disease, Symptom, Characteristic, AppUser, Temperature, SymptomOccurrence


class DiseaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disease
        fields = ('id', 'name', )


class SymptomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Symptom
        fields = ('id', 'name',)


class CharacteristicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Characteristic
        fields = ('id', 'name', 'question')


class AppUserSerializer(serializers.ModelSerializer):
    chars = CharacteristicSerializer(many=True, read_only=True)
    diseases = DiseaseSerializer(many=True, read_only=True)
    symptoms = SymptomSerializer(many=True, read_only=True)
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


class SymptomOccurrenceSerializer(serializers.ModelSerializer):
    symptom = SymptomSerializer()
    user = AppUserSerializer()

    class Meta:
        model = SymptomOccurrence
        fields = ('id', 'date', 'symptom', 'status', 'user')





