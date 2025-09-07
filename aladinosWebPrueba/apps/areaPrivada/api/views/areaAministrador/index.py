# views.py
from rest_framework import viewsets
from apps.areaPrivada.api.serializers.areaAministrador.index import LlamadaSerializer
from apps.areaPrivada.api.models.areaAministrador.index import RegistroLlamada
# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from apps.areaPrivada.api.models.areaAministrador.index import UserTrazability
from apps.areaPrivada.api.serializers.areaAministrador.index import UserTrazabilitySerializer
import logging
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny


logger = logging.getLogger(__name__)
class LlamadaViewSet(viewsets.ModelViewSet):
    queryset = RegistroLlamada.objects.all()
    serializer_class = LlamadaSerializer





logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])  # Permitir acceso sin autenticación
def trazability_list(request):
    """Obtener todos los registros de trazabilidad"""
    try:
        trazabilities = UserTrazability.objects.all().order_by('-entry_time')
        serializer = UserTrazabilitySerializer(trazabilities, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error obteniendo trazabilidad: {str(e)}")
        return Response(
            {'error': 'Error obteniendo datos de trazabilidad'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])  # Permitir acceso sin autenticación
def register_trazability_entry(request):
    """Registrar entrada de trazabilidad"""
    try:
        data = request.data.copy()
        
        # Añadir información del usuario si está autenticado
        if request.user.is_authenticated:
            data['user'] = request.user.id
        
        # Añadir IP del cliente
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            data['ip_address'] = x_forwarded_for.split(',')[0]
        else:
            data['ip_address'] = request.META.get('REMOTE_ADDR')
        
        data['entry_time'] = timezone.now()
        data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
        
        serializer = UserTrazabilitySerializer(data=data)
        if serializer.is_valid():
            trazability_entry = serializer.save()
            return Response({
                'success': True,
                'entry_id': trazability_entry.id,
                'message': 'Entrada registrada correctamente'
            })
        else:
            return Response(
                {'error': 'Datos inválidos', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        logger.error(f"Error registrando entrada de trazabilidad: {str(e)}")
        return Response(
            {'error': 'Error interno del servidor'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])  # Permitir acceso sin autenticación
def register_trazability_exit(request):
    """Registrar salida de trazabilidad"""
    try:
        entry_id = request.data.get('entry_id')
        if not entry_id:
            return Response(
                {'error': 'entry_id es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            trazability_entry = UserTrazability.objects.get(id=entry_id)
            trazability_entry.exit_time = timezone.now()
            trazability_entry.save()
            
            return Response({
                'success': True,
                'message': 'Salida registrada correctamente',
                'duration_seconds': trazability_entry.duration.total_seconds() if trazability_entry.duration else 0
            })
            
        except UserTrazability.DoesNotExist:
            return Response(
                {'error': 'Entrada no encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
    except Exception as e:
        logger.error(f"Error registrando salida de trazabilidad: {str(e)}")
        return Response(
            {'error': 'Error interno del servidor'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )