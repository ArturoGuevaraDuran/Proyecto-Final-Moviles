from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status

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