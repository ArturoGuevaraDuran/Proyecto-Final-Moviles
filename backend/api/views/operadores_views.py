from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from ..models import RegistroComida
import datetime

class EscanearQRView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 1. Validar que quien escanea sea un OPERADOR
        if request.user.rol != 'OPERADOR':
            return Response({"error": "Acceso denegado. Solo operadores pueden escanear."}, status=status.HTTP_403_FORBIDDEN)
        
        qr_leido = request.data.get('codigo_qr')
        if not qr_leido:
            return Response({"error": "No se proporcionó ningún código QR."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 2. Buscar el registro exacto usando el UUID del QR
            reserva = RegistroComida.objects.get(codigo_qr=qr_leido)
            
            # 3. Regla de Negocio: ¿Es un QR de un día anterior?
            hoy = datetime.date.today()
            if reserva.menu_diario.fecha != hoy:
                # Si el QR es viejo, lo marcamos como cancelado/vencido por seguridad
                if reserva.estado == 'RESERVADO':
                    reserva.estado = 'CANCELADO'
                    reserva.save()
                return Response({
                    "error": "QR Caducado", 
                    "detalle": f"Este código era para el {reserva.menu_diario.fecha}."
                }, status=status.HTTP_400_BAD_REQUEST)

            # 4. Regla de Negocio: ¿Ya le dieron su comida a este alumno?
            if reserva.estado == 'ENTREGADO':
                hora_entrega = reserva.fecha_hora_entrega.strftime("%H:%M hrs") if reserva.fecha_hora_entrega else "una hora desconocida"
                return Response({
                    "error": "QR Ya Usado",
                    "detalle": f"Esta comida ya fue entregada a las {hora_entrega}."
                }, status=status.HTTP_400_BAD_REQUEST)

            # 5. Si todo está perfecto, entregamos la comida (¡El caso de Éxito!)
            if reserva.estado == 'RESERVADO':
                reserva.estado = 'ENTREGADO'
                reserva.fecha_hora_entrega = timezone.now()
                reserva.save()
                
                return Response({
                    "mensaje": "Aprobado",
                    "alumno": f"{reserva.alumno.first_name} {reserva.alumno.last_name}",
                    "matricula": reserva.alumno.matricula,
                    "comida": reserva.menu_diario.descripcion
                }, status=status.HTTP_200_OK)
                
            # Por si acaso el estado es "Cancelado" manualmente por el admin
            return Response({"error": "QR Inválido", "detalle": f"El estado actual es: {reserva.estado}"}, status=status.HTTP_400_BAD_REQUEST)

        except RegistroComida.DoesNotExist:
            return Response({"error": "QR No Encontrado", "detalle": "El código escaneado no existe en el sistema."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Formato de QR inválido"}, status=status.HTTP_400_BAD_REQUEST)