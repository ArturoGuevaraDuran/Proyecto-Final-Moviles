from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views # Importamos la vista mágica de los tokens

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', views.obtain_auth_token, name='api_login'), # Creamos la ruta
]