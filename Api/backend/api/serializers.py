# api/serializers.py
from rest_framework import serializers
from django.utils import timezone
from .models import CustomUser, Trabajador, IngresoTrabajadores, SalidaTrabajadores


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('dni', 'apel_nomb', 'tipo_usuarioapp', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.apel_nomb = validated_data.get('apel_nomb', instance.apel_nomb)
        instance.tipo_usuarioapp = validated_data.get('tipo_usuarioapp', instance.tipo_usuarioapp)
        instance.save()
        return instance
    
    
from rest_framework import serializers
from .models import Trabajador

class TrabajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields = '__all__'



class IngresoTrabajadoresSerializer(serializers.ModelSerializer):
    fecha = serializers.DateField(read_only=True)
    hora = serializers.TimeField(required=False)
    

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Si el campo 'hora' no está presente en los datos, añadir la hora actual
        if 'hora' not in data:
            data['hora'] = timezone.now().time()
        return data

    class Meta:
        model = IngresoTrabajadores
        fields = ['trabajador', 'fecha', 'hora']


class SalidaTrabajadoresSerializer(serializers.ModelSerializer):
    fecha = serializers.DateField(read_only=True)
    hora = serializers.TimeField(required=False)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Si el campo 'hora' no está presente en los datos, añadir la hora actual
        if 'hora' not in data:
            data['hora'] = timezone.now().time()
        return data

    class Meta:
        model = SalidaTrabajadores
        fields = ['trabajador', 'fecha', 'hora']
        

class TrabajadorAsistenciasSerializer(serializers.ModelSerializer):
    apel_nomb = serializers.SerializerMethodField()

    class Meta:
        model = Trabajador
        fields = ['tipodoc', 'dni', 'apel_nomb']

    def get_apel_nomb(self, obj):
        return f"{obj.apel_paterno} {obj.apel_materno} {obj.nombre1} {obj.nombre2}".strip()


# En tu archivo serializers.py

from rest_framework import serializers
from .models import Trabajador, IngresoTrabajadores, SalidaTrabajadores

class AsistenciasFechaEspecificaSerializer(serializers.Serializer):
    trabajador = serializers.SerializerMethodField()
    ingresos = serializers.SerializerMethodField()
    salidas = serializers.SerializerMethodField()

    def get_trabajador(self, trabajador):
        return TrabajadorAsistenciasSerializer(trabajador).data

    def get_ingresos(self, trabajador):
        fecha_asistencias = self.context.get('fecha_asistencias')
        ingresos = IngresoTrabajadores.objects.filter(trabajador=trabajador, fecha=fecha_asistencias)
        return IngresoTrabajadoresSerializer(ingresos, many=True).data

    def get_salidas(self, trabajador):
        fecha_asistencias = self.context.get('fecha_asistencias')
        salidas = SalidaTrabajadores.objects.filter(trabajador=trabajador, fecha=fecha_asistencias)
        return SalidaTrabajadoresSerializer(salidas, many=True).data


from rest_framework import serializers
from .models import Especie

class EspecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especie
        fields = '__all__'

# MERLUZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

from rest_framework import serializers
from .models import Grupo_MERLUZA

class Grupo_MERLUZASerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo_MERLUZA
        fields = '__all__'


from rest_framework import serializers
from .models import Actividad_MERLUZA

class Actividad_MERLUZASerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad_MERLUZA
        fields = '__all__'


from rest_framework import serializers
from .models import Presentacion_MERLUZA

class Presentacion_MERLUZASerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentacion_MERLUZA
        fields = '__all__'


# POTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

from rest_framework import serializers
from .models import Grupo_POTA, Actividad_POTA, Presentacion_POTA

class Grupo_POTASerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo_POTA
        fields = '__all__'

class Actividad_POTASerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad_POTA
        fields = '__all__'

class Presentacion_POTASerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentacion_POTA
        fields = '__all__'


# serializers.py

from rest_framework import serializers
from .models import TrabajosRealizados

class TrabajosRealizadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrabajosRealizados
        fields = ['id', 'trabajador_dni', 'especie', 'grupo', 'actividad', 'presentacion', 'fecha', 'apel_nomb', 'Ndocumento', 'creado_por', 'kg']


class IngresoTrabajadoresSerializer(serializers.ModelSerializer):
    trabajador_dni = serializers.CharField(source='trabajador.dni', read_only=True)

    class Meta:
        model = IngresoTrabajadores
        fields = ['id', 'trabajador', 'trabajador_dni', 'fecha']

