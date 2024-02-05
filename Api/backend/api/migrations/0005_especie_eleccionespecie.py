# Generated by Django 5.0.1 on 2024-01-30 17:22

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_customuser_tipo_usuarioapp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Especie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(choices=[('E01', 'MERLUZA'), ('E02', 'POTA')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='EleccionEspecie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_ingreso', models.DateField(default=django.utils.timezone.now)),
                ('hora_ingreso', models.TimeField(default=django.utils.timezone.now)),
                ('id_contrato', models.CharField(choices=[('C01', 'C/PLANILLA'), ('C02', 'S/PLANILLA')], max_length=3)),
                ('contrato', models.CharField(choices=[('C01', 'C/PLANILLA'), ('C02', 'S/PLANILLA')], max_length=255)),
                ('id_grupo', models.CharField(choices=[('G01', 'OBRERO DESTAJO'), ('G02', 'OBRERO JORNAL')], max_length=3)),
                ('grupo', models.CharField(choices=[('G01', 'OBRERO DESTAJO'), ('G02', 'OBRERO JORNAL')], max_length=255)),
                ('id_actividad', models.CharField(choices=[('A01', 'FILETEO'), ('A02', 'SELECCIONADO'), ('A03', 'ENVASADO'), ('A04', 'HGT'), ('A05', 'SUPERVISOR'), ('A06', 'ABASTECIMIENTO'), ('A07', 'REVISADO'), ('A08', 'MOLIDO'), ('A09', 'LAVADO CANASTILLAS 3KG'), ('A10', 'LAVADO PLACAS 10KG'), ('A11', 'LAVADO AROS 7KG'), ('A12', 'GLASEADO'), ('A13', 'APUNTADOR'), ('A14', 'EMPACADO'), ('A15', 'PESADO'), ('A16', 'COCINA'), ('A17', 'APOYO'), ('A18', 'ALMACENAMIENTO'), ('A19', 'LAVADO FILETE'), ('A20', 'NUCA'), ('A21', 'TROQUELADO'), ('A22', 'PLAQUEADO'), ('A23', 'REHIELADO'), ('A24', 'ENVASADO FRESCOS'), ('A25', 'ENVASADO COCIDOS'), ('A26', 'LAMINADO'), ('A27', 'ABASTECIMIENTO FRESCO'), ('A28', 'ABASTECIMIENTO MP'), ('A29', 'PERFILADO'), ('A30', 'PALETEO'), ('A31', 'BAJADOR AROS 7KG')], max_length=3)),
                ('actividad', models.CharField(choices=[('A01', 'FILETEO'), ('A02', 'SELECCIONADO'), ('A03', 'ENVASADO'), ('A04', 'HGT'), ('A05', 'SUPERVISOR'), ('A06', 'ABASTECIMIENTO'), ('A07', 'REVISADO'), ('A08', 'MOLIDO'), ('A09', 'LAVADO CANASTILLAS 3KG'), ('A10', 'LAVADO PLACAS 10KG'), ('A11', 'LAVADO AROS 7KG'), ('A12', 'GLASEADO'), ('A13', 'APUNTADOR'), ('A14', 'EMPACADO'), ('A15', 'PESADO'), ('A16', 'COCINA'), ('A17', 'APOYO'), ('A18', 'ALMACENAMIENTO'), ('A19', 'LAVADO FILETE'), ('A20', 'NUCA'), ('A21', 'TROQUELADO'), ('A22', 'PLAQUEADO'), ('A23', 'REHIELADO'), ('A24', 'ENVASADO FRESCOS'), ('A25', 'ENVASADO COCIDOS'), ('A26', 'LAMINADO'), ('A27', 'ABASTECIMIENTO FRESCO'), ('A28', 'ABASTECIMIENTO MP'), ('A29', 'PERFILADO'), ('A30', 'PALETEO'), ('A31', 'BAJADOR AROS 7KG')], max_length=255)),
                ('id_presentacion', models.CharField(choices=[('P01', 'FILETE GOLD'), ('P02', 'FILETE PREMIUM'), ('P03', 'FILETE STD'), ('P04', 'HUEVERA'), ('P05', 'FILETE 133'), ('P06', 'FILETE 133 BP'), ('P07', 'TROZO'), ('P08', 'FILETE FB 200'), ('P09', 'CORTE HGT'), ('P10', 'ENVASADO HGT'), ('P11', 'APOYO'), ('P12', 'FILETEO'), ('P13', 'LAVADO FILETE'), ('P14', 'NUCA'), ('P15', 'ENVASADO FRESCOS'), ('P16', 'COCINA'), ('P17', 'TROQUELADO')], max_length=3)),
                ('presentacion', models.CharField(choices=[('P01', 'FILETE GOLD'), ('P02', 'FILETE PREMIUM'), ('P03', 'FILETE STD'), ('P04', 'HUEVERA'), ('P05', 'FILETE 133'), ('P06', 'FILETE 133 BP'), ('P07', 'TROZO'), ('P08', 'FILETE FB 200'), ('P09', 'CORTE HGT'), ('P10', 'ENVASADO HGT'), ('P11', 'APOYO'), ('P12', 'FILETEO'), ('P13', 'LAVADO FILETE'), ('P14', 'NUCA'), ('P15', 'ENVASADO FRESCOS'), ('P16', 'COCINA'), ('P17', 'TROQUELADO')], max_length=255)),
                ('fecha_salida', models.DateField(blank=True, null=True)),
                ('hora_salida', models.TimeField(blank=True, null=True)),
                ('trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.trabajador')),
                ('especie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.especie')),
            ],
            options={
                'unique_together': {('trabajador', 'fecha_ingreso')},
            },
        ),
    ]
