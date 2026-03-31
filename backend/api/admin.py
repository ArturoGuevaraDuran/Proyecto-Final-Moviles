from django.contrib import admin
from .models import Usuario, Facultad, Carrera, PuntoDistribucion, AsignacionOperador, MenuDiario, RegistroComida

# Registramos todos nuestros modelos para que aparezcan en el panel /admin
admin.site.register(Usuario)
admin.site.register(Facultad)
admin.site.register(Carrera)
admin.site.register(PuntoDistribucion)
admin.site.register(AsignacionOperador)
admin.site.register(MenuDiario)
admin.site.register(RegistroComida)