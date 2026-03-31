from rest_framework import serializers
from .models import Usuario, PuntoDistribucion, AsignacionOperador, MenuDiario, RegistroComida, Facultad, Carrera

class FacultadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facultad
        fields = '__all__'

class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    # Declaramos la edad para que el Serializer la extraiga de la @property
    edad = serializers.ReadOnlyField() 
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol', 'matricula', 
                  'curp', 'rfc', 'fecha_nacimiento', 'edad', 'telefono', 'facultad', 'carrera']
        extra_kwargs = {'password': {'write_only': True}}

class PuntoDistribucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuntoDistribucion
        fields = '__all__'

class AsignacionOperadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignacionOperador
        fields = '__all__'

class MenuDiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuDiario
        fields = '__all__'

class RegistroComidaSerializer(serializers.ModelSerializer):
    # Esto es opcional, pero ayuda a Angular a ver el código QR como texto string
    codigo_qr = serializers.UUIDField(format='hex_verbose', read_only=True)
    
    class Meta:
        model = RegistroComida
        fields = '__all__'