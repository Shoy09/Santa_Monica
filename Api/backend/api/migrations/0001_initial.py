# Generated by Django 5.0.1 on 2024-01-25 21:06

import api.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipodoc', models.CharField(choices=[('DNI', 'DNI'), ('CarnetExtranjeria', 'CARNET EXTRANJERIA')], max_length=20)),
                ('dni', models.CharField(max_length=20, unique=True, validators=[api.models.validate_numero_documento])),
                ('apel_paterno', models.CharField(max_length=255)),
                ('apel_materno', models.CharField(max_length=255)),
                ('nombre1', models.CharField(max_length=255)),
                ('nombre2', models.CharField(max_length=255)),
                ('apel_nomb', models.CharField(blank=True, max_length=1020)),
                ('flag_sexo', models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino')], max_length=1)),
                ('estado_civil', models.CharField(blank=True, max_length=255, null=True)),
                ('fec_nacimiento', models.DateField(blank=True, null=True)),
                ('grado_instruccion', models.CharField(blank=True, max_length=255, null=True)),
                ('provincia', models.CharField(blank=True, max_length=255, null=True)),
                ('distrito', models.CharField(blank=True, max_length=255, null=True)),
                ('departamento', models.CharField(blank=True, max_length=255, null=True)),
                ('nrohijos', models.IntegerField(blank=True, null=True)),
                ('cargo', models.CharField(blank=True, max_length=255, null=True)),
                ('tipo_trabajador', models.CharField(blank=True, max_length=255, null=True)),
                ('condicion', models.CharField(blank=True, max_length=255, null=True)),
                ('centro_costo', models.CharField(blank=True, max_length=255, null=True)),
                ('area', models.CharField(choices=[('PRODUCCION', 'Producción'), ('ADMINISTRACION', 'Administración')], max_length=255)),
                ('seccion', models.CharField(blank=True, max_length=255, null=True)),
                ('empresa', models.CharField(blank=True, max_length=255, null=True)),
                ('fec_ingreso', models.DateField(blank=True, null=True)),
                ('fec_cese', models.DateField(blank=True, null=True)),
                ('telefono1', models.CharField(blank=True, max_length=20, null=True)),
                ('situacion_trabajador', models.CharField(blank=True, max_length=255, null=True)),
                ('afp', models.CharField(blank=True, max_length=255, null=True)),
                ('nro_afp_trabaj', models.CharField(blank=True, max_length=255, null=True)),
                ('flag_comision_afp', models.BooleanField(blank=True, null=True)),
                ('banco_haberes', models.CharField(blank=True, max_length=255, null=True)),
                ('cuenta_haberes', models.CharField(blank=True, max_length=255, null=True)),
                ('tipo_cnta_haberes', models.CharField(blank=True, max_length=255, null=True)),
                ('cod_moneda', models.CharField(blank=True, max_length=3, null=True)),
                ('banco_cts', models.CharField(blank=True, max_length=255, null=True)),
                ('moneda_cts', models.CharField(blank=True, max_length=3, null=True)),
                ('nro_cnta_cts', models.CharField(blank=True, max_length=255, null=True)),
                ('regimen_laboral', models.CharField(blank=True, max_length=255, null=True)),
                ('flag_essalud_vida', models.BooleanField(blank=True, null=True)),
                ('turno', models.CharField(blank=True, max_length=255, null=True)),
                ('tipo_contrato', models.CharField(blank=True, max_length=255, null=True)),
                ('periocidad', models.CharField(max_length=255)),
                ('sindicalizado', models.BooleanField(blank=True, null=True)),
                ('tipo_pago_cts_boleta', models.CharField(blank=True, max_length=255, null=True)),
                ('estado', models.CharField(choices=[('CESADO', 'Cesado'), ('INACTIVO', 'Inactivo'), ('ACTIVO', 'Activo'), ('CESADO-REVISAR', 'Cesado-Revisar')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('tipo_usuarioapp', models.CharField(choices=[('Administrador', 'Administrador'), ('EmpleadoGarita', 'Empleado Garita'), ('EmpleadoProcesoPota', 'Empleado Proceso Pota'), ('EmpleadoProcesoMerluza', 'Empleado Proceso Merluza')], default='EmpleadoGarita', max_length=25)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('dni', models.CharField(max_length=12, unique=True, validators=[api.models.validate_dni_length])),
                ('apel_nomb', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SalidaTrabajadores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('hora', models.TimeField(default=django.utils.timezone.now)),
                ('trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.trabajador', to_field='dni')),
            ],
        ),
        migrations.CreateModel(
            name='IngresoTrabajadores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('hora', models.TimeField(default=django.utils.timezone.now)),
                ('trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.trabajador', to_field='dni')),
            ],
        ),
    ]
