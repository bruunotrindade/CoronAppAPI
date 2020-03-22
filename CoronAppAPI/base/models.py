from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Disease(BaseModel):
    name = models.CharField(verbose_name="Nome", max_length=60)

    class Meta:
        verbose_name = "Doença"


class Symptom(BaseModel):
    name = models.CharField(verbose_name="Nome", max_length=60)

    class Meta:
        verbose_name = "Sintoma"


class Characteristic(BaseModel):
    name = models.CharField(verbose_name="Nome", max_length=60)
    question = models.CharField(verbose_name="Pergunta", max_length=100)

    class Meta:
        verbose_name = "Característica"


class AppUser(BaseModel):
    email = models.EmailField()
    dob = models.DateField(verbose_name="Data de nascimento")
    state = models.CharField(verbose_name="Estado", max_length=16)
    city = models.CharField(verbose_name="Cidade", max_length=40)
    chars = models.ManyToManyField(Characteristic, verbose_name="Características")
    diseases = models.ManyToManyField(Disease, verbose_name="Doenças")
    symptoms = models.ManyToManyField(Symptom, verbose_name="Sintomas")

    class Meta:
        verbose_name = "Usuário"


class Temperature(BaseModel):
    value = models.FloatField(verbose_name="Valor", max_length=60)
    date = models.DateTimeField(verbose_name="Data") 
    user = models.ForeignKey(AppUser, verbose_name="Usuário", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Medição de Temperatura"
        verbose_name_plural = "Medições de Temperatura"
    

class SymptomOccurrence(BaseModel):
    BEGIN = "I"
    END = "F"
    STATUS_CHOICES = [
        (BEGIN, "Início"),
        (END, "Final")
    ]

    date = models.DateTimeField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    symptom = models.ForeignKey(Symptom, verbose_name="Sintoma", on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, verbose_name="Usuário", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ocorrência de Sintoma"
        verbose_name_plural = "Ocorrências de Sintomas"

