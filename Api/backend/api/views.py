from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.http import JsonResponse
from datetime import datetime, timedelta

from .models import CustomUser, Trabajador
from .serializers import CustomUserSerializer, TrabajadorSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Usar AllowAny solo para la acción 'create'
        if self.action == 'create':
            self.permission_classes = [AllowAny]

        return super().get_permissions()

    def perform_create(self, serializer):
        # Guarda el nuevo usuario
        user = serializer.save()

        # Genera un token para el usuario
        refresh = RefreshToken.for_user(user)

        # Agrega el token a la respuesta
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

class ObtainTokenView(APIView):
    def post(self, request):
        dni = request.data.get('dni')
        password = request.data.get('password')

        user = authenticate(request, dni=dni, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'id': user.id,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCurrentUser(request):
    user = request.user

    # Utiliza tu propio serializador para CustomUser
    user_serializer = CustomUserSerializer(user)

    user_data = {
        'id': user.id,
        'dni': user.dni,
        'apel_nomb': user.apel_nomb,
        'tipo_usuarioapp': user.tipo_usuarioapp,
        'is_active': user.is_active,
        'is_staff': user.is_staff,
        'date_joined': user.date_joined,
        # Agrega otros campos según tu modelo de usuario
    }

    return JsonResponse(user_data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_usuario(request, dni):
    try:
        usuario = CustomUser.objects.get(dni=dni)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    usuario.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_usuario(request, dni):
    try:
        usuario = CustomUser.objects.get(dni=dni)
    except CustomUser.DoesNotExist:
        return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # Elimina la contraseña de los datos de la solicitud si está presente
        if 'password' in request.data:
            del request.data['password']

        serializer = CustomUserSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer

class UserByDniAPIView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        dni = self.kwargs.get('dni')
        try:
            user = CustomUser.objects.get(dni=dni)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        

class TrabajadorViewSet(viewsets.ModelViewSet):
    queryset = Trabajador.objects.all()
    serializer_class = TrabajadorSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    def get_permissions(self):
        # Agregar permisos personalizados si es necesario
        return super().get_permissions()
    


# api/views.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = get_object_or_404(CustomUser, id=request.user.id)
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)


from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_lista_usuarios(request):
    usuarios = CustomUser.objects.all()
    serializer = CustomUserSerializer(usuarios, many=True)
    return Response(serializer.data)

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_tipos_usuarios(request):
    tipos_usuarios = [choice[1] for choice in CustomUser.TipoUsuario.choices]
    return JsonResponse({'tipos_usuarios': tipos_usuarios})


from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import IngresoTrabajadores, SalidaTrabajadores
from .serializers import IngresoTrabajadoresSerializer, SalidaTrabajadoresSerializer
from datetime import date
from django.utils import timezone


class IngresoTrabajadoresViewSet(viewsets.ModelViewSet):
    queryset = IngresoTrabajadores.objects.all()
    serializer_class = IngresoTrabajadoresSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Configura la fecha y hora correctamente al crear un nuevo ingreso
        serializer.save(fecha=timezone.localtime(timezone.now()).date(), hora=timezone.localtime(timezone.now()).time())
    
    @action(detail=False, methods=['get'])
    def ingresos_hoy(self, request):
        # Obtén los ingresos del día actual
        ingresos = IngresoTrabajadores.objects.filter(fecha=timezone.now().date())
        serializer = IngresoTrabajadoresSerializer(ingresos, many=True)
        return Response(serializer.data)

class SalidaTrabajadoresViewSet(viewsets.ModelViewSet):
    queryset = SalidaTrabajadores.objects.all()
    serializer_class = SalidaTrabajadoresSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Configura la fecha y hora correctamente al crear una nueva salida
        serializer.save(fecha=timezone.localtime(timezone.now()).date(), hora=timezone.localtime(timezone.now()).time())

    @action(detail=False, methods=['get'])
    def salidas_hoy(self, request):
        # Obtener las salidas del día actual
        salidas = SalidaTrabajadores.objects.filter(fecha=timezone.now().date())
        serializer = SalidaTrabajadoresSerializer(salidas, many=True)
        return Response(serializer.data)
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Trabajador, IngresoTrabajadores, SalidaTrabajadores
from .serializers import TrabajadorAsistenciasSerializer, IngresoTrabajadoresSerializer, SalidaTrabajadoresSerializer
from datetime import date, timedelta


class TrabajadorAsistenciasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, trabajador_dni=None, fecha=None):
        try:
            # Obtener el trabajador por DNI o todos los trabajadores si no se proporciona un DNI
            if trabajador_dni:
                trabajadores = [Trabajador.objects.get(dni=trabajador_dni)]
            else:
                trabajadores = Trabajador.objects.all()

            # Inicializar una lista para almacenar las asistencias por trabajador
            asistencias_por_trabajador = []

            # Obtener las asistencias del trabajador para el mes de la fecha proporcionada
            for trabajador in trabajadores:
                # Convertir la fecha a formato Date
                if fecha:
                    fecha_asistencias = date.fromisoformat(str(fecha))
                else:
                    # Asignar un valor predeterminado o manejar el caso sin fecha
                    fecha_asistencias = date.today()

                # Calcular el primer y último día del mes
                primer_dia_mes = fecha_asistencias.replace(day=1)
                ultimo_dia_mes = fecha_asistencias.replace(day=28) + timedelta(days=4)
                ultimo_dia_mes = ultimo_dia_mes - timedelta(days=ultimo_dia_mes.day)

                # Filtrar ingresos y salidas para el mes
                ingresos = IngresoTrabajadores.objects.filter(
                    trabajador=trabajador,
                    fecha__range=(primer_dia_mes, ultimo_dia_mes)
                )
                salidas = SalidaTrabajadores.objects.filter(
                    trabajador=trabajador,
                    fecha__range=(primer_dia_mes, ultimo_dia_mes)
                )

                # Serializar las asistencias
                ingresos_serializer = IngresoTrabajadoresSerializer(ingresos, many=True)
                salidas_serializer = SalidaTrabajadoresSerializer(salidas, many=True)

                # Almacenar las asistencias en la lista por trabajador
                asistencias_por_trabajador.append({
                    'trabajador': TrabajadorAsistenciasSerializer(trabajador).data,
                    'ingresos': ingresos_serializer.data,
                    'salidas': salidas_serializer.data,
                })

            # Construir la respuesta
            response_data = {
                'asistencias': asistencias_por_trabajador,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Trabajador.DoesNotExist:
            return Response({'error': 'Trabajador no encontrado'}, status=status.HTTP_404_NOT_FOUND)


# En tu archivo views.py
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Trabajador, IngresoTrabajadores, SalidaTrabajadores
from .serializers import (
    TrabajadorAsistenciasSerializer,
    IngresoTrabajadoresSerializer,
    SalidaTrabajadoresSerializer,
)
from rest_framework.permissions import IsAuthenticated
from datetime import date, timedelta

class AsistenciasFechaEspecificaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, fecha=None):
        try:
            # Inicializar una lista para almacenar las asistencias por trabajador
            asistencias_por_trabajador = []

            # Obtener las asistencias del trabajador para la fecha proporcionada
            trabajadores_con_asistencias = Trabajador.objects.filter(
                ingresotrabajadores__fecha=fecha
            ).distinct() | Trabajador.objects.filter(
                salidatrabajadores__fecha=fecha
            ).distinct()

            for trabajador in trabajadores_con_asistencias:
                ingresos = IngresoTrabajadores.objects.filter(
                    trabajador=trabajador,
                    fecha=fecha
                )
                salidas = SalidaTrabajadores.objects.filter(
                    trabajador=trabajador,
                    fecha=fecha
                )

                ingresos_serializer = IngresoTrabajadoresSerializer(ingresos, many=True)
                salidas_serializer = SalidaTrabajadoresSerializer(salidas, many=True)

                asistencias_por_trabajador.append({
                    'trabajador': TrabajadorAsistenciasSerializer(trabajador).data,
                    'ingresos': ingresos_serializer.data,
                    'salidas': salidas_serializer.data,
                })

            # Construir la respuesta
            response_data = {
                'asistencias': asistencias_por_trabajador,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Trabajador.DoesNotExist:
            return Response({'error': 'Trabajador no encontrado'}, status=status.HTTP_404_NOT_FOUND)


# En tu archivo views.py
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Trabajador, IngresoTrabajadores, SalidaTrabajadores
from .serializers import (
    TrabajadorAsistenciasSerializer,
    IngresoTrabajadoresSerializer,
    SalidaTrabajadoresSerializer,
)
from rest_framework.permissions import IsAuthenticated
from datetime import date, timedelta, datetime

class AsistenciasFechaActualView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Obtener la fecha actual
            fecha_actual = datetime.now().date()

            # Inicializar una lista para almacenar las asistencias por trabajador
            asistencias_por_trabajador = []

            # Obtener las asistencias del trabajador para la fecha actual
            trabajadores_con_asistencias = Trabajador.objects.filter(
                ingresotrabajadores__fecha=fecha_actual
            ).distinct() | Trabajador.objects.filter(
                salidatrabajadores__fecha=fecha_actual
            ).distinct()

            for trabajador in trabajadores_con_asistencias:
                ingresos = IngresoTrabajadores.objects.filter(
                    trabajador=trabajador,
                    fecha=fecha_actual
                )
                salidas = SalidaTrabajadores.objects.filter(
                    trabajador=trabajador,
                    fecha=fecha_actual
                )

                ingresos_serializer = IngresoTrabajadoresSerializer(ingresos, many=True)
                salidas_serializer = SalidaTrabajadoresSerializer(salidas, many=True)

                asistencias_por_trabajador.append({
                    'trabajador': TrabajadorAsistenciasSerializer(trabajador).data,
                    'ingresos': ingresos_serializer.data,
                    'salidas': salidas_serializer.data,
                })

            # Construir la respuesta
            response_data = {
                'asistencias': asistencias_por_trabajador,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Trabajador.DoesNotExist:
            return Response({'error': 'Trabajador no encontrado'}, status=status.HTTP_404_NOT_FOUND)


from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import CustomUser

@require_GET
def buscar_nombre_por_dni(request):
    dni = request.GET.get('dni')

    print(f"Intentando buscar el nombre para el DNI: {dni}")

    # Eliminamos cualquier carácter no numérico del DNI
    dni = ''.join(c for c in dni if c.isdigit())

    if dni is None or not dni.isdigit() or (len(dni) != 8 and len(dni) != 12):
        print("DNI inválido")
        return JsonResponse({'error': 'DNI inválido'}, status=400)

    try:
        # Convertimos el DNI a un número para manejar ceros iniciales
        dni_numeric = int(dni)
        usuario = CustomUser.objects.get(dni=dni_numeric)
        nombre = usuario.apel_nomb
        print(f"Nombre encontrado: {nombre}")
        return JsonResponse({'nombre': nombre})
    except CustomUser.DoesNotExist:
        print("Usuario no encontrado")
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    except ValueError:
        print("Error al convertir DNI a número")
        return JsonResponse({'error': 'DNI inválido'}, status=400)



from rest_framework import generics
from .models import Especie
from .serializers import EspecieSerializer

class EspecieCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        especie_data = request.data
        especie_nombre = especie_data.get('especie', None)

        if especie_nombre:
            existing_especie = Especie.objects.filter(especie=especie_nombre).first()
            if existing_especie:
                return Response({'error': 'La especie ya existe.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = EspecieSerializer(data=especie_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'El nombre de la especie es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

class EspecieListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Especie.objects.all()
    serializer_class = EspecieSerializer

class EspecieRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Especie.objects.all()
    serializer_class = EspecieSerializer

# MERLUZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

from rest_framework import generics
from .models import Grupo_MERLUZA
from .serializers import Grupo_MERLUZASerializer

class Grupo_MERLUZAListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Grupo_MERLUZA.objects.all()
    serializer_class = Grupo_MERLUZASerializer

class Grupo_MERLUZARetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Grupo_MERLUZA.objects.all()
    serializer_class = Grupo_MERLUZASerializer


from rest_framework import generics
from .models import Actividad_MERLUZA
from .serializers import Actividad_MERLUZASerializer

class Actividad_MERLUZACreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        actividad_nombre = request.data.get('actividad', None)

        if actividad_nombre:
            existing_actividad = Actividad_MERLUZA.objects.filter(actividad=actividad_nombre).first()
            if existing_actividad:
                return Response({'error': 'La actividad ya existe.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = Actividad_MERLUZASerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'El nombre de la actividad es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

class Actividad_MERLUZARetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Actividad_MERLUZA.objects.all()
    serializer_class = Actividad_MERLUZASerializer


class Actividad_MERLUZAListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Actividad_MERLUZA.objects.all()
    serializer_class = Actividad_MERLUZASerializer

from rest_framework import generics, status
from rest_framework.response import Response
from .models import Presentacion_MERLUZA
from .serializers import Presentacion_MERLUZASerializer

class Presentacion_MERLUZAListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Presentacion_MERLUZA.objects.all()
    serializer_class = Presentacion_MERLUZASerializer

    def post(self, request, *args, **kwargs):
        presentacion_nombre = request.data.get('presentacion', None)

        if presentacion_nombre:
            existing_presentacion = Presentacion_MERLUZA.objects.filter(presentacion=presentacion_nombre).first()
            if existing_presentacion:
                return Response({'error': 'La presentación ya existe.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'El nombre de la presentación es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class Presentacion_MERLUZARetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Presentacion_MERLUZA.objects.all()
    serializer_class = Presentacion_MERLUZASerializer


# POTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Grupo_POTA, Actividad_POTA, Presentacion_POTA
from .serializers import Grupo_POTASerializer, Actividad_POTASerializer, Presentacion_POTASerializer

class Grupo_POTAListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Grupo_POTA.objects.all()
    serializer_class = Grupo_POTASerializer

class Grupo_POTARetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Grupo_POTA.objects.all()
    serializer_class = Grupo_POTASerializer

class Actividad_POTACreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        actividad_nombre = request.data.get('actividad', None)

        if actividad_nombre:
            existing_actividad = Actividad_POTA.objects.filter(actividad=actividad_nombre).first()
            if existing_actividad:
                return Response({'error': 'La actividad ya existe.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = Actividad_POTASerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'El nombre de la actividad es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

class Actividad_POTARetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Actividad_POTA.objects.all()
    serializer_class = Actividad_POTASerializer

class Actividad_POTAListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Actividad_POTA.objects.all()
    serializer_class = Actividad_POTASerializer

class Presentacion_POTAListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Presentacion_POTA.objects.all()
    serializer_class = Presentacion_POTASerializer

    def post(self, request, *args, **kwargs):
        presentacion_nombre = request.data.get('presentacion', None)

        if presentacion_nombre:
            existing_presentacion = Presentacion_POTA.objects.filter(presentacion=presentacion_nombre).first()
            if existing_presentacion:
                return Response({'error': 'La presentación ya existe.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'El nombre de la presentación es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class Presentacion_POTARetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Presentacion_POTA.objects.all()
    serializer_class = Presentacion_POTASerializer


from rest_framework import generics, status
from rest_framework.response import Response
from .models import TrabajosRealizados
from .serializers import TrabajosRealizadosSerializer

class TrabajosRealizadosListAPIView(generics.ListAPIView):
    queryset = TrabajosRealizados.objects.all()
    serializer_class = TrabajosRealizadosSerializer

from rest_framework.permissions import IsAuthenticated

class TrabajosRealizadosCreateAPIView(generics.CreateAPIView):
    serializer_class = TrabajosRealizadosSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Obtener el DNI del trabajador desde la solicitud
        trabajador_dni = request.data.get('trabajador_dni')

        # Validar si el trabajador existe por su DNI
        trabajador = Trabajador.objects.filter(dni=trabajador_dni).first()
        if not trabajador:
            return Response({"error": f"No se encontró ningún trabajador con el DNI {trabajador_dni}"},
                            status=status.HTTP_404_NOT_FOUND)

        # Verificar si el trabajador está en el área de PRODUCCION
        if trabajador.area != 'PRODUCCION':
            return Response({"error": "El trabajador debe pertenecer al área de PRODUCCION para registrar un trabajo."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Verificar si hay un ingreso previo para el trabajador en la fecha actual
        ingreso_existente = IngresoTrabajadores.objects.filter(trabajador=trabajador, fecha=date.today()).exists()
        if not ingreso_existente:
            return Response({"error": "No se puede registrar el trabajo sin un ingreso previo para este trabajador hoy."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Verificar si ya existe un registro para este trabajador en la misma fecha
        trabajo_existente = TrabajosRealizados.objects.filter(trabajador_dni=trabajador.id, fecha=date.today()).exists()
        if trabajo_existente:
            return Response({"error": "Ya existe un registro para este trabajador en la fecha actual."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Agregar el ID del trabajador y el nombre del usuario autenticado a los datos de la solicitud
        request.data['trabajador_dni'] = trabajador.id
        request.data['creado_por'] = request.user.apel_nomb

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TrabajosRealizadosDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TrabajosRealizados.objects.all()
    serializer_class = TrabajosRealizadosSerializer


from datetime import datetime

class TrabajosRealizadosDetalleAPIView(APIView):
    serializer_class = TrabajosRealizadosSerializer

    def get(self, request, dni, *args, **kwargs):
        # Obtener el queryset de trabajos realizados para el trabajador
        trabajos_realizados = TrabajosRealizados.objects.filter(trabajador_dni__dni=dni)

        # Obtener la fecha de ingreso del trabajador
        ingreso_trabajador = IngresoTrabajadores.objects.filter(trabajador__dni=dni).first()
        fecha_ingreso = ingreso_trabajador.fecha if ingreso_trabajador else None

        # Obtener la fecha de salida del trabajador
        salida_trabajador = SalidaTrabajadores.objects.filter(trabajador__dni=dni).first()
        fecha_salida = salida_trabajador.fecha if salida_trabajador else None

        # Obtener el mes actual
        mes_actual = datetime.now().month

        # Filtrar los trabajos realizados por el mes actual
        trabajos_realizados = trabajos_realizados.filter(fecha__month=mes_actual)

        serializer = self.serializer_class(trabajos_realizados, many=True)
        data = {
            'fecha_ingreso': fecha_ingreso,
            'trabajos_realizados': serializer.data,
            'fecha_salida': fecha_salida
        }
        return Response(data)

from datetime import datetime
from django.db.models import Q

class TrabajosRealizadosPorMesAPIView(APIView):
    serializer_class = TrabajosRealizadosSerializer

    def get(self, request, fecha, *args, **kwargs):
        try:
            # Convertir la fecha proporcionada a un objeto de fecha
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
            # Obtener el mes de la fecha proporcionada
            mes = fecha_obj.month
            # Obtener el año de la fecha proporcionada
            año = fecha_obj.year
        except ValueError:
            return Response({"error": "La fecha proporcionada no es válida."}, status=400)

        # Filtrar los trabajos realizados para el mes y año proporcionados
        trabajos_realizados = TrabajosRealizados.objects.filter(fecha__year=año, fecha__month=mes)

        serializer = self.serializer_class(trabajos_realizados, many=True)
        return Response(serializer.data)



from rest_framework.views import APIView
from rest_framework.response import Response
from .models import IngresoTrabajadores, TrabajosRealizados, SalidaTrabajadores
from .serializers import IngresoTrabajadoresSerializer, TrabajosRealizadosSerializer
from datetime import date

class TrabajadoresIngresadosHoyAPIView(APIView):
    serializer_class = TrabajosRealizadosSerializer

    def get(self, request, *args, **kwargs):
        # Obtener la fecha actual
        fecha_actual = date.today()

        # Obtener los ingresos de los trabajadores de producción que ocurrieron hoy
        ingresos_produccion = IngresoTrabajadores.objects.filter(fecha=fecha_actual, trabajador__area='PRODUCCION')

        # Obtener los trabajos realizados asociados a los ingresos de los trabajadores de producción
        trabajos_realizados = []
        for ingreso in ingresos_produccion:
            trabajos_ingreso = TrabajosRealizados.objects.filter(trabajador_dni=ingreso.trabajador, fecha=fecha_actual)
            trabajos_realizados.extend(trabajos_ingreso)

        # Obtener las salidas de los trabajadores de producción que ocurrieron hoy
        salidas_produccion = SalidaTrabajadores.objects.filter(fecha=fecha_actual, trabajador__area='PRODUCCION')

        # Serializar los ingresos, trabajos realizados y salidas
        ingresos_serializer = IngresoTrabajadoresSerializer(ingresos_produccion, many=True)
        trabajos_serializer = self.serializer_class(trabajos_realizados, many=True)
        salidas_serializer = SalidaTrabajadoresSerializer(salidas_produccion, many=True)

        # Construir la respuesta
        data = {
            'ingresos': ingresos_serializer.data,
            'trabajos_realizados': trabajos_serializer.data,
            'salidas': salidas_serializer.data
        }

        return Response(data)
    def put(self, request, *args, **kwargs):
        # Obtener los datos de la solicitud PUT
        datos_actualizados = request.data

        # Obtener el DNI del trabajador a actualizar
        dni_trabajador = kwargs.get('dni')

        # Buscar el objeto a actualizar por DNI del trabajador
        try:
            objeto_a_actualizar = TrabajosRealizados.objects.get(trabajador_dni=dni_trabajador)
        except TrabajosRealizados.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Serializar y validar los datos actualizados
        serializer = TrabajosRealizadosSerializer(objeto_a_actualizar, data=datos_actualizados)
        if serializer.is_valid():
            # Guardar los datos actualizados en la base de datos
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
