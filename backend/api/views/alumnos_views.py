from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import MenuDiario, RegistroComida
from ..serializers import MenuDiarioSerializer, RegistroComidaSerializer
import datetime

class MenuDisponibleView(APIView):
    # EXIGIMOS que el usuario tenga un token válido para entrar aquí
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Validar que el usuario sea ALUMNO
        if request.user.rol != 'ALUMNO':
            return Response({"error": "Solo los alumnos pueden ver el menú disponible."}, status=status.HTTP_403_FORBIDDEN)
        
        # Buscar la comida del día de hoy que NO esté agotada
        hoy = datetime.date.today()
        menus = MenuDiario.objects.filter(fecha=hoy).exclude(estado_disponibilidad='AGOTADA')
        
        # Convertir los modelos de Django a JSON usando nuestro Serializer
        serializer = MenuDiarioSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReservarComidaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.rol != 'ALUMNO':
            return Response({"error": "Solo los alumnos pueden reservar comida."}, status=status.HTTP_403_FORBIDDEN)
        
        menu_id = request.data.get('menu_id')
        
        try:
            menu = MenuDiario.objects.get(id=menu_id)
        except MenuDiario.DoesNotExist:
            return Response({"error": "El menú seleccionado no existe."}, status=status.HTTP_404_NOT_FOUND)
            
        # REGLA DE NEGOCIO: Verificar si el alumno ya reservó hoy
        hoy = datetime.date.today()
        ya_reservo = RegistroComida.objects.filter(alumno=request.user, menu_diario__fecha=hoy).exists()
        
        if ya_reservo:
            return Response({"error": "Ya tienes una reserva o comida entregada para el día de hoy."}, status=status.HTTP_400_BAD_REQUEST)
            
        # Crear la reserva (Esto automáticamente generará el UUID para el código QR)
        reserva = RegistroComida.objects.create(
            alumno=request.user,
            menu_diario=menu,
            estado='RESERVADO'
        )
        
        serializer = RegistroComidaSerializer(reserva)
        return Response(serializer.data, status=status.HTTP_201_CREATED)