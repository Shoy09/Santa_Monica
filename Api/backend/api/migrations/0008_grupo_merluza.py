# Generated by Django 5.0.1 on 2024-01-31 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_especie'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grupo_MERLUZA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grupo', models.CharField(max_length=100)),
            ],
        ),
    ]