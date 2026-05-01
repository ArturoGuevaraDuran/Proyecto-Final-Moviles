from django.urls import path

from api.views.admin_views import GenerarTokenOperadorView, AdminMetricasView
from api.views.operadores_views import EscanearQRView
from .views.auth_views import CatalogosView, LoginView, RegistroAlumnoView, RegistroOperadorView
from .views.alumnos_views import MenuDisponibleView, ReservarComidaView

urlpatterns = [
    # Esta ruta coincidirá exactamente con lo que espera Angular
    #Auth / inicio de sesion
    path('login/', LoginView.as_view(), name='api-login'),
    path('registro/alumno/', RegistroAlumnoView.as_view(), name='api-registro-alumno'),
    path('registro/operador/', RegistroOperadorView.as_view(), name='api-registro-operador'),
    
    # Alumnos
    path('alumnos/menu/', MenuDisponibleView.as_view(), name='api-alumnos-menu'),
    path('alumnos/reservar/', ReservarComidaView.as_view(), name='api-alumnos-reservar'),
    
    # Operadores
    path('operadores/escanear/', EscanearQRView.as_view(), name='api-operadores-escanear'),
    
    # Admin
    path('admin/metricas/', AdminMetricasView.as_view(), name='admin-metricas'),
    path('admin/generar-token/', GenerarTokenOperadorView.as_view(), name='admin-generar-token'),
    
    # Carreras / Facultades
    path('catalogos/', CatalogosView.as_view(), name='api-catalogos'),
]