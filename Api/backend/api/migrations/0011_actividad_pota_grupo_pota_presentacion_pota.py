# Generated by Django 5.0.1 on 2024-01-31 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_presentacion_merluza'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad_POTA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actividad', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo_POTA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grupo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Presentacion_POTA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presentacion', models.CharField(max_length=100)),
            ],
        ),
    ]
