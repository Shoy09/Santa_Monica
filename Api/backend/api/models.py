# api/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

def validate_dni_length(value):
    if len(value) not in [8, 12]:
        raise ValidationError(
            ('El DNI debe tener 8 o 12 dígitos.'),
            code='invalid_dni_length'
        )
class CustomUserManager(BaseUserManager):
    def _create_user(self, dni, apel_nomb, password=None, **extra_fields):
        if not dni:
            raise ValueError('El campo DNI es obligatorio.')

        user = self.model(
            dni=dni,
            apel_nomb=apel_nomb,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, dni, apel_nomb, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(dni, apel_nomb, password, **extra_fields)

    def create_superuser(self, dni, apel_nomb, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(dni, apel_nomb, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    class TipoUsuario(models.TextChoices):
        ADMINISTRADOR = 'Administrador', 'Administrador'
        EMPLEADO_GARITA = 'Garita', 'Garita'
        EMPLEADO_PROCESO_POTA = 'Proceso Pota', 'Proceso Pota'
        EMPLEADO_PROCESO_MERLOZA = 'Proceso Merluza', 'Proceso Merluza'

    # Aumenta el valor de max_length acomodando la longitud del valor más largo en choices
    tipo_usuarioapp = models.CharField(
        max_length=25,  # o el valor necesario para acomodar "EmpleadoProcesoMerloza"
        choices=TipoUsuario.choices,
        default=TipoUsuario.EMPLEADO_GARITA
    )

    id = models.BigAutoField(primary_key=True)
    dni = models.CharField(
        unique=True,
        max_length=12,
        validators=[validate_dni_length]  # Añade la validación personalizada
    )
    apel_nomb = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['apel_nomb', 'tipo_usuarioapp']

    def __str__(self):
        return f'{self.apel_nomb} ({self.dni})'


# models.py

from django.core.exceptions import ValidationError
from django.db import models

class Trabajador(models.Model):
    DNI = 'DNI'
    CARNET_EXTRANJERIA = 'Carnet de Extranjería'  # Modificado aquí

    TIPODOC_CHOICES = [
        (DNI, 'DNI'),
        (CARNET_EXTRANJERIA, 'Carnet de Extranjería'),  # Modificado aquí
    ]
    SEXO_CHOICES = [
        ('F', 'Femenino'),
        ('M', 'Masculino'),
    ]
    AREA_CHOICES = [
        ('PRODUCCION', 'Producción'),
        ('ADMINISTRACION', 'Administración'),
    ]
    ESTADO_CHOICES = [
        ('CESADO', 'Cesado'),
        ('INACTIVO', 'Inactivo'),
        ('ACTIVO', 'Activo'),
        ('CESADO-REVISAR', 'Cesado-Revisar'),
    ]
    tipodoc = models.CharField(max_length=26, choices=TIPODOC_CHOICES)
    dni = models.CharField(max_length=20, unique=True, validators=[])
    apel_paterno = models.CharField(max_length=255)
    apel_materno = models.CharField(max_length=255)
    nombre1 = models.CharField(max_length=255)
    nombre2 = models.CharField(max_length=255)
    apel_nomb = models.CharField(max_length=1020, blank=True)
    flag_sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    estado_civil = models.CharField(max_length=255, null=True, blank=True)
    fec_nacimiento = models.DateField(null=True, blank=True)
    grado_instruccion = models.CharField(max_length=255, null=True, blank=True)
    provincia = models.CharField(max_length=255, null=True, blank=True)
    distrito = models.CharField(max_length=255, null=True, blank=True)
    departamento = models.CharField(max_length=255, null=True, blank=True)
    nrohijos = models.IntegerField(null=True, blank=True)
    cargo = models.CharField(max_length=255, null=True, blank=True)
    tipo_trabajador = models.CharField(max_length=255, null=True, blank=True)
    condicion = models.CharField(max_length=255, null=True, blank=True)
    centro_costo = models.CharField(max_length=255, null=True, blank=True)
    area = models.CharField(max_length=255, choices=AREA_CHOICES)
    seccion = models.CharField(max_length=255, null=True, blank=True)
    empresa = models.CharField(max_length=255, null=True, blank=True)
    fec_ingreso = models.DateField(null=True, blank=True)
    fec_cese = models.DateField(null=True, blank=True)
    telefono1 = models.CharField(max_length=20, null=True, blank=True)
    situacion_trabajador = models.CharField(max_length=255, null=True, blank=True)
    afp = models.CharField(max_length=255, null=True, blank=True)
    nro_afp_trabaj = models.CharField(max_length=255, null=True, blank=True)
    flag_comision_afp = models.BooleanField(null=True, blank=True)
    banco_haberes = models.CharField(max_length=255, null=True, blank=True)
    cuenta_haberes = models.CharField(max_length=255, null=True, blank=True)
    tipo_cnta_haberes = models.CharField(max_length=255, null=True, blank=True)
    cod_moneda = models.CharField(max_length=3, null=True, blank=True)
    banco_cts = models.CharField(max_length=255, null=True, blank=True)
    moneda_cts = models.CharField(max_length=3, null=True, blank=True)
    nro_cnta_cts = models.CharField(max_length=255, null=True, blank=True)
    regimen_laboral = models.CharField(max_length=255, null=True, blank=True)
    flag_essalud_vida = models.BooleanField(null=True, blank=True)
    turno = models.CharField(max_length=255, null=True, blank=True)
    tipo_contrato = models.CharField(max_length=255, null=True, blank=True)
    periocidad = models.CharField(max_length=255, null=True, blank=True)
    sindicalizado = models.BooleanField(null=True, blank=True)
    tipo_pago_cts_boleta = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=255, choices=ESTADO_CHOICES)

    def save(self, *args, **kwargs):
        # Completar apel_nomb con la combinación de apellidos y nombres
        self.apel_nomb = f"{self.apel_paterno} {self.apel_materno} {self.nombre1} {self.nombre2}".strip()
        super().save(*args, **kwargs)

    def clean(self):
        validate_numero_documento(self.dni, self.tipodoc)

    def __str__(self):
        return f"{self.nombre1} {self.apel_paterno}"
    

def validate_numero_documento(value, tipo_documento):
    if tipo_documento == Trabajador.DNI:
        if not value.isdigit() or len(value) != 8:
            raise ValidationError("El DNI debe contener 8 dígitos numéricos.")
    elif tipo_documento == Trabajador.CARNET_EXTRANJERIA:
        if not value.isdigit() or len(value) != 12:
            raise ValidationError("El Carnet de Extranjería debe contener 12 dígitos numéricos.")
    # Puedes agregar más validaciones para otros tipos de documentos aquí


from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Trabajador


class IngresoTrabajadores(models.Model):
    trabajador = models.ForeignKey(Trabajador, to_field='dni', on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)

    def clean(self):
        # Verificar que el ingreso para el trabajador en la fecha actual no exista
        existing_ingreso = IngresoTrabajadores.objects.filter(trabajador=self.trabajador, fecha=self.fecha)
        if existing_ingreso.exists():
            raise ValidationError('El ingreso ya fue registrado para este trabajador en la fecha actual.')

    def save(self, *args, **kwargs):
        self.clean()  # Llama a la función clean antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ingreso de {self.trabajador} el {self.fecha} a las {self.hora}"

class SalidaTrabajadores(models.Model):
    trabajador = models.ForeignKey(Trabajador,to_field='dni', on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)

    def clean(self):
        # Verificar que exista un ingreso previo para este trabajador en la fecha actual
        existing_ingreso = IngresoTrabajadores.objects.filter(trabajador=self.trabajador, fecha=self.fecha)
        if not existing_ingreso.exists():
            raise ValidationError('No se puede registrar la salida sin un ingreso previo para este trabajador en la fecha actual.')

        # Verificar que la salida para el trabajador en la fecha actual no exista
        existing_salida = SalidaTrabajadores.objects.filter(trabajador=self.trabajador, fecha=self.fecha)
        if existing_salida.exists():
            raise ValidationError('La salida ya fue registrada para este trabajador en la fecha actual.')

    def save(self, *args, **kwargs):
        self.clean()  # Llama a la función clean antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Salida de {self.trabajador} el {self.fecha} a las {self.hora}"


class Especie(models.Model):
    especie = models.CharField(max_length=100)

    def __str__(self):
        return self.especie
    

# MERLUZAAAAA
class Grupo_MERLUZA(models.Model):
    grupo = models.CharField(max_length=100)

    def __str__(self):
        return self.grupo
    

class Actividad_MERLUZA(models.Model):
    actividad = models.CharField(max_length=100)

    def __str__(self):
        return self.actividad


class Presentacion_MERLUZA(models.Model):
    presentacion = models.CharField(max_length=100)

    def __str__(self):
        return self.presentacion
    
# POTAAAAAAA
    
class Grupo_POTA(models.Model):
    grupo = models.CharField(max_length=100)

    def __str__(self):
        return self.grupo

class Actividad_POTA(models.Model):
    actividad = models.CharField(max_length=100)

    def __str__(self):
        return self.actividad


class Presentacion_POTA(models.Model):
    presentacion = models.CharField(max_length=100)

    def __str__(self):
        return self.presentacion



from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Trabajador, IngresoTrabajadores, SalidaTrabajadores, Especie
from django.contrib.auth.models import User

class TrabajosRealizados(models.Model):
    trabajador_dni = models.ForeignKey(Trabajador, on_delete=models.CASCADE, db_column='trabajador_dni')
    especie = models.CharField(max_length=255)  
    grupo = models.CharField(max_length=100)
    actividad = models.CharField(max_length=100)
    presentacion = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    apel_nomb = models.CharField(max_length=1020, blank=True)
    Ndocumento = models.CharField(max_length=255, blank=True)
    creado_por = models.CharField(max_length=255, blank=True)
    kg = models.CharField(max_length=255, null=True, blank=True)  # Permitir que el campo sea nulo
    
    def clean(self):
        if self.trabajador_dni.area != 'PRODUCCION':
            raise ValidationError('Solo se pueden agregar trabajadores del área de PRODUCCION.')

        # Verificar que exista un ingreso previo para el trabajador en la fecha actual
        existing_ingreso = IngresoTrabajadores.objects.filter(trabajador=self.trabajador_dni, fecha=self.fecha)
        if not existing_ingreso.exists():
            raise ValidationError('No se puede registrar el trabajo sin un ingreso previo para este trabajador en la fecha actual.')

        # Verificar que no exista una salida previa para el trabajador en la fecha actual
        existing_salida = SalidaTrabajadores.objects.filter(trabajador=self.trabajador_dni, fecha=self.fecha)
        if existing_salida.exists():
            raise ValidationError('No se puede registrar el trabajo si ya se ha registrado la salida para este trabajador en la fecha actual.')

    def save(self, *args, **kwargs):
        # Llenar el campo apel_nomb con los datos del trabajador asociado si existe
        if self.trabajador_dni_id:
            self.apel_nomb = self.trabajador_dni.apel_nomb
            self.Ndocumento = self.trabajador_dni.dni 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Trabajo realizado por {self.apel_nomb} ({self.trabajador_dni.dni}) el {self.fecha}"
