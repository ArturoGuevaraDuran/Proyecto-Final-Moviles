from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.signing import TimestampSigner

class InvitarOperadorView(APIView):
    # Protegido, solo si mandan Token de sesión
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Doble candado: Asegurar que sea el ADMIN
        if request.user.rol != 'ADMIN':
            return Response({"error": "Solo el administrador puede invitar operadores."}, status=status.HTTP_403_FORBIDDEN)

        email_operador = request.data.get('email')
        if not email_operador:
            return Response({"error": "Debe proporcionar el correo del operador a invitar."}, status=status.HTTP_400_BAD_REQUEST)

        # Generar un token seguro y encriptado con el correo
        signer = TimestampSigner()
        token_seguro = signer.sign(email_operador)

        # En un proyecto real, aquí usaríamos send_mail() de Django para mandarlo.
        # Por ahora, se lo devolvemos al frontend del admin para que lo copie o simule el envío.
        enlace_invitacion = f"http://localhost:4200/registro-operador?token={token_seguro}"

        return Response({
            "mensaje": "Invitación generada correctamente.",
            "email_destino": email_operador,
            "token": token_seguro,
            "enlace_frontend": enlace_invitacion
        }, status=status.HTTP_200_OK)