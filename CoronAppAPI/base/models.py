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

    def __str__(self):
        return f'{self.name}'


class Symptom(BaseModel):
    UNCOMMON = 'U'
    COMMON = 'C'

    TYPE_SYMPTOMS = [
        (UNCOMMON, 'Incomum'),
        (COMMON, 'Comum'),
    ]

    name = models.CharField(verbose_name="Nome", max_length=60)
    type_symptom = models.CharField(verbose_name="Tipo de Sintoma", max_length=1, choices=TYPE_SYMPTOMS)

    class Meta:
        verbose_name = "Sintoma"

    def __str__(self):
        return f'{self.name}'


class Characteristic(BaseModel):
    name = models.CharField(verbose_name="Nome", max_length=60)
    question = models.CharField(verbose_name="Pergunta", max_length=100)

    class Meta:
        verbose_name = "Característica"

    def __str__(self):
        return f'Name: {self.name}, Question: {self.question}'


class AppUser(BaseModel):
    email = models.EmailField()
    dob = models.DateField(verbose_name="Data de nascimento")
    state = models.CharField(verbose_name="Estado", max_length=16)
    city = models.CharField(verbose_name="Cidade", max_length=40)
    chars = models.ManyToManyField(Characteristic, verbose_name="Características")
    diseases = models.ManyToManyField(Disease, verbose_name="Doenças")
    symptoms = models.ManyToManyField(Symptom, verbose_name="Sintomas", through='SymptomOccurrence')

    class Meta:
        verbose_name = "Usuário"

    def __str__(self):
        return f'{self.email}'


# class UserSymptoms(BaseModel):
#     created_at = models.DateField(auto_now_add=True)
#     user = models.ForeignKey(AppUser, verbose_name='Usuário', on_delete=models.CASCADE)
#     symptom = models.ForeignKey(Symptom, verbose_name='Sintoma', on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = 'Sintoma do Usuário'
#         verbose_name_plural = 'Sintomas dos Usuários'
#
#     def __str__(self):
#         return f'User: {self.user}, Sintoma: {self.symptom}'


class Temperature(BaseModel):
    value = models.FloatField(verbose_name="Valor", max_length=60)
    date = models.DateTimeField(verbose_name="Data") 
    user = models.ForeignKey(AppUser, verbose_name="Usuário", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Medição de Temperatura"
        verbose_name_plural = "Medições de Temperatura"

    def __str__(self):
        return f'User: {self.user}'
    

class SymptomOccurrence(BaseModel):
    start_date = models.DateTimeField(verbose_name='Data de Inicio do Sintoma')
    end_date = models.DateTimeField(verbose_name='Data de Termino do Sintoma', null=True, blank=True)
    symptom = models.ForeignKey(Symptom, verbose_name="Sintoma", on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, verbose_name="Usuário", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ocorrência de Sintoma"
        verbose_name_plural = "Ocorrências de Sintomas"

    def __str__(self):
        return f'User: {self.user}, Status: Inicio({self.start_date}), Fim({self.end_date if self.end_date else ""})'


class Recommendation(BaseModel):
    name = models.CharField(verbose_name='Nome', max_length=150)
    texto = models.TextField(verbose_name='Texto')
    symptoms = models.ManyToManyField(Symptom, verbose_name='Sintomas', related_name='recommendations_set')
    diseases = models.ManyToManyField(Disease, verbose_name='Doenças', related_name='recommendations_set')
    characteristics = models.ManyToManyField(
        Characteristic, verbose_name='Caracteristicas', related_name='recommendations_set'
    )

    class Meta:
        verbose_name = 'Recomendação'
        verbose_name_plural = 'Recomendações'

    def __str__(self):
        return f'{self.name}'




