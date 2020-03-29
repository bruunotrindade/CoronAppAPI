from rest_framework import serializers

from base.models import (
    Disease, Symptom, Characteristic, AppUser, Temperature, SymptomOccurrence
)


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = ('id', 'name',)


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


class SymptomOccurrenceCreateSerializer(serializers.Serializer):
    idUser = serializers.PrimaryKeyRelatedField(queryset=AppUser.objects.all())
    symptoms = serializers.JSONField(required=True)

    def create(self, validated_data):
        from django.utils import timezone
        symptoms_data = validated_data.pop('symptoms')
        user = validated_data.pop('idUser')

        symptoms_actives = SymptomOccurrence.objects.filter(user=user, end_date__isnull=True)
        new_actives = []
        if len(symptoms_data) > 0:
            for active in symptoms_actives:
                if str(active.symptom_id) not in [symptom['id'] for symptom in symptoms_data]:
                    active.end_date = timezone.now()
                    active.save()
                else:
                    new_actives.append(active)

        data = []
        if len(symptoms_data) > 0:
            for item in symptoms_data:
                if item['id'] not in [str(occurrence.symptom_id) for occurrence in new_actives]:
                    try:
                        data.append(SymptomOccurrence(symptom_id=item['id'], user=user, start_date=item['start_date']))
                    except KeyError:
                        data.append(SymptomOccurrence(symptom_id=item['id'], user=user, start_date=timezone.now()))
        else:
            return SymptomOccurrence.objects.create(
                user=user, symptom=None, start_date=timezone.now().date())

        return SymptomOccurrence.objects.bulk_create(data)


class SymptomOccurrenceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='symptom.id')
    name = serializers.ReadOnlyField(source='symptom.name')
    type = serializers.ReadOnlyField(source='symptom.get_type_symptom_display')

    class Meta:
        model = SymptomOccurrence
        fields = ('id', 'start_date', 'end_date', 'symptom', 'type', 'name')


class AppUserSerializer(serializers.ModelSerializer):
    chars = CharacteristicSerializer(many=True, read_only=True)
    diseases = DiseaseSerializer(many=True, read_only=True)
    symptoms = SymptomOccurrenceSerializer(source='symptomoccurrence_set', many=True, read_only=True)
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
