from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
import uuid

# 1. Catálogo de Facultades
class Facultad(models.Model):
    nombre = models.CharField(max_length=150, unique=True) # Ej: Facultad de Ciencias de la Computación

    def __str__(self):
        return self.nombre

# 2. Catálogo de Carreras
class Carrera(models.Model):
    nombre = models.CharField(max_length=150) # Ej: Ingeniería en Tecnologías de la Información
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name='carreras')

    def __str__(self):
        return self.nombre

# 3. Usuario Actualizado
class Usuario(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('OPERADOR', 'Operador'),
        ('ALUMNO', 'Alumno'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='ALUMNO')
    matricula = models.CharField(max_length=20, blank=True, null=True)
    
    # Nuevos campos fiscales/identidad
    curp = models.CharField(max_length=18, blank=True, null=True, unique=True)
    rfc = models.CharField(max_length=13, blank=True, null=True, unique=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    
    # Relaciones foráneas a los catálogos
    facultad = models.ForeignKey(Facultad, on_delete=models.SET_NULL, blank=True, null=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, blank=True, null=True)

    # Cálculo dinámico de la edad (No se guarda en la BD)
    @property
    def edad(self):
        if self.fecha_nacimiento:
            hoy = date.today()
            # Resta los años y ajusta si el cumpleaños de este año aún no ha pasado
            return hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return None

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"


class PuntoDistribucion(models.Model):
    nombre = models.CharField(max_length=100) # Ej. "Carrito Ingeniería"
    latitud = models.FloatField()
    longitud = models.FloatField()
    disponibilidad = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class AsignacionOperador(models.Model):
    operador = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'OPERADOR'})
    punto_distribucion = models.ForeignKey(PuntoDistribucion, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f"{self.operador.username} en {self.punto_distribucion.nombre}"


class MenuDiario(models.Model):
    ESTADOS_COMIDA = (
        ('ALTA', 'Alta (Hay mucha)'),
        ('MEDIA', 'Media (Queda la mitad)'),
        ('BAJA', 'Baja (Por acabarse)'),
        ('AGOTADA', 'Agotada'),
    )
    TURNOS = (
        ('DESAYUNO', 'Desayuno'),
        ('COMIDA', 'Comida'),
    )
    
    punto_distribucion = models.ForeignKey(PuntoDistribucion, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True) # Para saber de qué día es este menú
    turno = models.CharField(max_length=10, choices=TURNOS)
    descripcion = models.TextField() # Ej. "Chilaquiles con pollo"
    estado_disponibilidad = models.CharField(max_length=10, choices=ESTADOS_COMIDA, default='ALTA')
    foto_evidencia = models.URLField(blank=True, null=True) # URL de Supabase Storage

    def __str__(self):
        return f"{self.turno} - {self.punto_distribucion.nombre} ({self.fecha})"


class RegistroComida(models.Model):
    ESTADOS_RESERVA = (
        ('RESERVADO', 'Reservado'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    )
    
    alumno = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'ALUMNO'})
    menu_diario = models.ForeignKey(MenuDiario, on_delete=models.CASCADE)
    codigo_qr = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    estado = models.CharField(max_length=15, choices=ESTADOS_RESERVA, default='RESERVADO')
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    fecha_hora_entrega = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Reserva {self.alumno.username} - {self.estado}"