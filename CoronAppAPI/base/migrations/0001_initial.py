# Generated by Django 3.0.3 on 2020-03-28 02:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('dob', models.DateField(verbose_name='Data de nascimento')),
                ('state', models.CharField(max_length=16, verbose_name='Estado')),
                ('city', models.CharField(max_length=40, verbose_name='Cidade')),
            ],
            options={
                'verbose_name': 'Usuário',
            },
        ),
        migrations.CreateModel(
            name='Characteristic',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60, verbose_name='Nome')),
                ('question', models.CharField(max_length=100, verbose_name='Pergunta')),
            ],
            options={
                'verbose_name': 'Característica',
            },
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Doença',
            },
        ),
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60, verbose_name='Nome')),
                ('type_symptom', models.CharField(choices=[('U', 'Incomum'), ('C', 'Comum')], max_length=1, verbose_name='Tipo de Sintoma')),
            ],
            options={
                'verbose_name': 'Sintoma',
            },
        ),
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('value', models.FloatField(max_length=60, verbose_name='Valor')),
                ('date', models.DateTimeField(verbose_name='Data')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.AppUser', verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Medição de Temperatura',
                'verbose_name_plural': 'Medições de Temperatura',
            },
        ),
        migrations.CreateModel(
            name='SymptomOccurrence',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField(verbose_name='Data de Inicio do Sintoma')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='Data de Termino do Sintoma')),
                ('symptom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Symptom', verbose_name='Sintoma')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.AppUser', verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Ocorrência de Sintoma',
                'verbose_name_plural': 'Ocorrências de Sintomas',
            },
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, verbose_name='Nome')),
                ('texto', models.TextField(verbose_name='Texto')),
                ('characteristics', models.ManyToManyField(related_name='recommendations_set', to='base.Characteristic', verbose_name='Caracteristicas')),
                ('diseases', models.ManyToManyField(related_name='recommendations_set', to='base.Disease', verbose_name='Doenças')),
                ('symptoms', models.ManyToManyField(related_name='recommendations_set', to='base.Symptom', verbose_name='Sintomas')),
            ],
            options={
                'verbose_name': 'Recomendação',
                'verbose_name_plural': 'Recomendações',
            },
        ),
        migrations.AddField(
            model_name='appuser',
            name='chars',
            field=models.ManyToManyField(to='base.Characteristic', verbose_name='Características'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='diseases',
            field=models.ManyToManyField(to='base.Disease', verbose_name='Doenças'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='symptoms',
            field=models.ManyToManyField(through='base.SymptomOccurrence', to='base.Symptom', verbose_name='Sintomas'),
        ),
    ]
