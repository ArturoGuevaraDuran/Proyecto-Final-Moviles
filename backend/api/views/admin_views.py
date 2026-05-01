from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
import uuid
from api.models import RegistroComida, InvitacionOperador

class AdminMetricasView(APIView):
    # Protegido, solo si mandan Token de sesión
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        # Candado: Asegurar que sea el ADMIN usando tu sistema de roles
        if getattr(request.user, 'rol', '') != 'ADMIN':
            return Response({"error": "No tienes permisos para ver las métricas."}, status=status.HTTP_403_FORBIDDEN)

        hoy = timezone.now().date()
        
        # Filtramos las comidas del día de hoy
        reservas_hoy = RegistroComida.objects.filter(fecha_reserva__date=hoy) 
        
        total = reservas_hoy.count()
        entregadas = reservas_hoy.filter(estado='ENTREGADO').count()
        pendientes = reservas_hoy.filter(estado='RESERVADO').count()

        return Response({
            "totalReservas": total,
            "entregadas": entregadas,
            "pendientes": pendientes
        })

class GenerarTokenOperadorView(APIView):
    # Protegido, solo si mandan Token de sesión
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Doble candado: Asegurar que sea el ADMIN
        if getattr(request.user, 'rol', '') != 'ADMIN':
            return Response({"error": "Solo el administrador puede generar códigos de invitación."}, status=status.HTTP_403_FORBIDDEN)

        # Generamos un código criptográfico corto estilo "OP-A1B2C3D4-BUAP"
        random_hex = uuid.uuid4().hex[:8].upper()
        codigo = f"OP-{random_hex}-BUAP"
        
        # Lo guardamos en la base de datos para que el operador lo pueda canjear después
        InvitacionOperador.objects.create(codigo=codigo)
        
        return Response({
            "mensaje": "Invitación generada correctamente.",
            "codigo": codigo
        }, status=status.HTTP_201_CREATED)