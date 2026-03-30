from django.urls import path
from .views.auth_views import LoginView
from .views.alumnos_views import MenuDisponibleView, ReservarComidaView

urlpatterns = [
    # Esta ruta coincidirá exactamente con lo que espera Angular
    #Auth / inicio de sesion
    path('login/', LoginView.as_view(), name='api-login'),
    
    # Alumnos
    path('alumnos/menu/', MenuDisponibleView.as_view(), name='api-alumnos-menu'),
    path('alumnos/reservar/', ReservarComidaView.as_view(), name='api-alumnos-reservar'),
]