from api.serializers import CarreraSerializer, FacultadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from ..models import Carrera, Facultad, Usuario, InvitacionOperador

class CatalogosView(APIView):
    permission_classes = []

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

        # Validación Correo institucional
        if not email or not email.endswith('@alumno.buap.mx'):
            return Response({"error": "Debe usar un correo institucional @alumno.buap.mx"}, status=status.HTTP_400_BAD_REQUEST)

        # Validación Que no exista ya
        if Usuario.objects.filter(username=email).exists() or Usuario.objects.filter(email=email).exists():
            return Response({"error": "Este correo ya está registrado."}, status=status.HTTP_400_BAD_REQUEST)

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
    # Público, porque apenas se van a registrar
    permission_classes = [] 

    def post(self, request):
        data = request.data
        codigo_invitacion = data.get('codigo_invitacion')
        email = data.get('email')
        password = data.get('password')

        # Validar que vengan los datos esenciales
        if not codigo_invitacion or not email or not password:
            return Response({"error": "Faltan datos requeridos (código, email o contraseña)."}, status=status.HTTP_400_BAD_REQUEST)

        # Validar que el código de invitación exista y no esté usado
        invitacion = InvitacionOperador.objects.filter(codigo=codigo_invitacion, usado=False).first()
        if not invitacion:
            return Response({"error": "El código de invitación es inválido o ya fue utilizado."}, status=status.HTTP_400_BAD_REQUEST)

        # Validar que el correo no esté registrado previamente
        if Usuario.objects.filter(username=email).exists() or Usuario.objects.filter(email=email).exists():
            return Response({"error": "Este correo ya está registrado en el sistema."}, status=status.HTTP_400_BAD_REQUEST)

        # Crear al operador con todos tus campos personalizados
        user = Usuario.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=data.get('nombre', ''),
            last_name=data.get('apellidos', ''),
            telefono=data.get('telefono', ''),
            curp=data.get('curp', ''),
            rfc=data.get('rfc', ''), 
            fecha_nacimiento=data.get('fecha_nacimiento'),
            rol='OPERADOR'
        )

        # Quemar el código para evitar que otro se registre con él
        invitacion.usado = True
        invitacion.save()

        return Response({"mensaje": "Operador configurado exitosamente. Ya puede iniciar sesión."}, status=status.HTTP_201_CREATED)