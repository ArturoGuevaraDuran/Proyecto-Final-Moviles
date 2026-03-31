from api.serializers import CarreraSerializer, FacultadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from ..models import Carrera, Facultad, Usuario

class CatalogosView(APIView):
    permission_classes = [] # Público, para que Angular arme el formulario de registro

    def get(self, request):
        facultades = Facultad.objects.all()
        carreras = Carrera.objects.all()
        
        return Response({
            "facultades": FacultadSerializer(facultades, many=True).data,
            "carreras": CarreraSerializer(carreras, many=True).data
        }, status=status.HTTP_200_OK)

class LoginView(APIView):
    # Este endpoint debe ser público, cualquiera puede intentar iniciar sesión
    permission_classes = [] 

    def post(self, request):
        # Angular nos manda 'username' y 'password' (recordemos que el frontend mapeó el email/matrícula a username)
        username = request.data.get('username')
        password = request.data.get('password')

        # Django verifica si las credenciales coinciden con las encriptadas en la BD
        user = authenticate(username=username, password=password)

        if user:
            if not user.is_active:
                return Response({"error": "Esta cuenta está desactivada."}, status=status.HTTP_403_FORBIDDEN)
            
            # Si el usuario es correcto, obtenemos su token (o le creamos uno si no tiene)
            token, created = Token.objects.get_or_create(user=user)
            
            # Le mandamos a Angular todo lo que necesita para armar su interfaz
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'rol': user.rol,
                'nombre': user.first_name,
                'apellidos': user.last_name
            }, status=status.HTTP_200_OK)
            
        else:
            # Si falla, mandamos un error 401 Unauthorized
            return Response({"error": "Credenciales incorrectas"}, status=status.HTTP_401_UNAUTHORIZED)
        
class RegistroAlumnoView(APIView):
    # Cualquiera puede intentar registrarse
    permission_classes = [] 

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        matricula = request.data.get('matricula')

        # 1. Validación de negocio: Correo institucional
        if not email or not email.endswith('@alumno.buap.mx'):
            return Response({"error": "Debe usar un correo institucional @alumno.buap.mx"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Validación: Que no exista ya
        if Usuario.objects.filter(username=email).exists() or Usuario.objects.filter(email=email).exists():
            return Response({"error": "Este correo ya está registrado."}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Crear el usuario ALUMNO (Usamos el email como username para facilitar el login)
        user = Usuario.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=request.data.get('nombre', ''),
            last_name=request.data.get('apellidos', ''),
            matricula=matricula,
            curp=request.data.get('curp'),                 # CURP del alumno
            fecha_nacimiento=request.data.get('fecha_nacimiento'), # Fecha para calcular edad
            facultad_id=request.data.get('facultad_id'),   # Relación foránea
            carrera_id=request.data.get('carrera_id'),     # Relación foránea
            rol='ALUMNO'
        )
        return Response({"mensaje": "Alumno registrado exitosamente"}, status=status.HTTP_201_CREATED)


class RegistroOperadorView(APIView):
    # Público, pero protegido criptográficamente por el Token
    permission_classes = [] 

    def post(self, request):
        token_invitacion = request.data.get('token')
        password = request.data.get('password')

        if not token_invitacion or not password:
            return Response({"error": "Faltan datos requeridos (token o password)."}, status=status.HTTP_400_BAD_REQUEST)

        signer = TimestampSigner()
        try:
            # Desencriptar el token, máximo 24 horas (86400 segundos) de validez
            email = signer.unsign(token_invitacion, max_age=86400)
        except SignatureExpired:
            return Response({"error": "El enlace de invitación ha expirado (Tienen 24 horas de validez)."}, status=status.HTTP_400_BAD_REQUEST)
        except BadSignature:
            return Response({"error": "Token de invitación inválido o corrupto."}, status=status.HTTP_400_BAD_REQUEST)

        if Usuario.objects.filter(username=email).exists():
            return Response({"error": "Este operador ya fue registrado anteriormente."}, status=status.HTTP_400_BAD_REQUEST)

        # Crear al operador
        user = Usuario.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=request.data.get('nombre', ''),
            last_name=request.data.get('apellidos', ''),
            telefono=request.data.get('telefono', ''),
            curp=request.data.get('curp'),                 # CURP del trabajador
            rfc=request.data.get('rfc'),                   # ¡Aquí SÍ va el RFC!
            fecha_nacimiento=request.data.get('fecha_nacimiento'),
            rol='OPERADOR'
        )
        return Response({"mensaje": "Operador configurado exitosamente. Ya puede iniciar sesión."}, status=status.HTTP_201_CREATED)