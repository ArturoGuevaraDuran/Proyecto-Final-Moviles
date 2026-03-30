from rest_framework import serializers
from .models import Usuario, PuntoDistribucion, AsignacionOperador, MenuDiario, RegistroComida

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol', 'matricula', 'facultad', 'telefono', 'fecha_nacimiento']
        # Protegemos el password para que nunca se envíe al frontend
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