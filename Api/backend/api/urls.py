# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register(r'usuarios', CustomUserViewSet, basename='usuario')
router.register(r'trabajadores', TrabajadorViewSet, basename='trabajador')
router.register(r'ingresos', IngresoTrabajadoresViewSet, basename='ingreso')
router.register(r'salidas', SalidaTrabajadoresViewSet, basename='salida')


urlpatterns = [
    path('', include(router.urls)),
    path('trabajadores/<int:pk>/detalles-ingreso-salida/', TrabajadorViewSet.as_view({'get': 'detalles_ingreso_salida'}), name='trabajador-detalles-ingreso-salida'),
    path('token/', ObtainTokenView.as_view(), name='obtain_token'),
    path('usuarios/', CustomUserViewSet.as_view({'post': 'create'}), name='create_user'),
    path('usuarios/eliminar/<str:dni>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/actualizar/<str:dni>/', actualizar_usuario, name='actualizar_usuario'),
    path('usuarios/dni/<str:dni>/', UserByDniAPIView.as_view(), name='user-by-dni'),
    path('current_user/', current_user, name='current_user'),
    path('tipoUsuarios/', obtener_tipos_usuarios, name='obtener_tipos_usuarios'),
    path('asistencias/<int:trabajador_dni>/', TrabajadorAsistenciasView.as_view(), name='trabajador_asistencias'),
    path('asistencias/<str:trabajador_dni>/<str:fecha>/', TrabajadorAsistenciasView.as_view(), name='trabajador_asistencias'),
    path('asistencias/<str:fecha>/', AsistenciasFechaEspecificaView.as_view(), name='asistencias-fecha-especifica'),
    path('asistencias-fecha-actual/', AsistenciasFechaActualView.as_view(), name='asistencias-fecha-actual'),
    path('buscar_nombre_por_dni/', buscar_nombre_por_dni, name='buscar_nombre_por_dni'),  
    path('especies/', EspecieListAPIView.as_view(), name='especie-list'),
    path('especies/<int:pk>/', EspecieRetrieveUpdateDestroyAPIView.as_view(), name='especie-detail'),
    path('especies/crear/', EspecieCreateAPIView.as_view(), name='crear-especie'),
    path('MERLUZA/grupos/', Grupo_MERLUZAListCreateAPIView.as_view(), name='grupo_merluza-list-create'),
    path('MERLUZA/grupos/<int:pk>/', Grupo_MERLUZARetrieveUpdateDestroyAPIView.as_view(), name='grupo_merluza-detail'),
    path('MERLUZA/actividades/crear/', Actividad_MERLUZACreateAPIView.as_view(), name='actividad_merluza-list-create'),
    path('MERLUZA/actividades/<int:pk>/', Actividad_MERLUZARetrieveUpdateDestroyAPIView.as_view(), name='actividad_merluza-detail'),
    path('MERLUZA/actividades/', Actividad_MERLUZAListAPIView.as_view(), name='actividad_merluza-list'),
    path('MERLUZA/presentaciones/', Presentacion_MERLUZAListCreateAPIView.as_view(), name='presentacion_merluza-list-create'),
    path('MERLUZA/presentaciones/<int:pk>/', Presentacion_MERLUZARetrieveUpdateDestroyAPIView.as_view(), name='presentacion_merluza-detail'),
    path('POTA/grupos/', Grupo_POTAListCreateAPIView.as_view(), name='grupo_pota-list-create'),
    path('pota/grupos/<int:pk>/', Grupo_POTARetrieveUpdateDestroyAPIView.as_view(), name='grupo_pota-detail'),
    path('pota/actividades/crear/', Actividad_POTACreateAPIView.as_view(), name='actividad_pota-list-create'),
    path('pota/actividades/<int:pk>/', Actividad_POTARetrieveUpdateDestroyAPIView.as_view(), name='actividad_pota-detail'),
    path('POTA/actividades/', Actividad_POTAListAPIView.as_view(), name='actividad_pota-list'),
    path('POTA/presentaciones/', Presentacion_POTAListCreateAPIView.as_view(), name='presentacion_pota-list-create'),
    path('pota/presentaciones/<int:pk>/', Presentacion_POTARetrieveUpdateDestroyAPIView.as_view(), name='presentacion_pota-detail'),
    path('trabajos_realizados/', TrabajosRealizadosListAPIView.as_view(), name='trabajos_realizados-list'),
    path('trabajos_realizados/create/', TrabajosRealizadosCreateAPIView.as_view(), name='trabajos_realizados-create'),
    path('trabajos_realizados/<int:pk>/', TrabajosRealizadosDetailUpdateDeleteAPIView.as_view(), name='trabajos_realizados-detail'),
    # path('trabajos_realizados/<str:dni>/', views.TrabajosRealizadosDetalleAPIView.as_view(), name='trabajos_realizados-detalle'),
    path('trabajos_realizados/<str:dni>/mes/', views.TrabajosRealizadosDetalleAPIView.as_view(), name='trabajos_realizados-mes'),
    # path('trabajos_realizados/<str:fecha>/', views.TrabajosRealizadosPorMesAPIView.as_view(), name='trabajos_realizados-mes'),
    path('trabajadores/Proceso/hoy/', TrabajadoresIngresadosHoyAPIView.as_view(), name='trabajadores_ingresados_hoy'),
    path('trabajadores/Proceso/hoy/<str:dni>/', TrabajadoresIngresadosHoyAPIView.as_view(), name='trabajadores_ingresados_hoy'),
    ]
