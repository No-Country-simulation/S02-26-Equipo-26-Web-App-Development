from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.users.models import Caregiver
from .serializers import CaregiverSerializer


class CaregiverViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Caregivers.
    
    IMPORTANTE: Caregiver usa user_id como primary key.
    Las URLs usan el user_id, no un id separado.
    
    Endpoints disponibles:
    - GET /api/caregivers/ → Listar todos los cuidadores
    - GET /api/caregivers/user_id/ → Ver detalle de un cuidador
    - PATCH /api/caregivers/user_id/ → Actualizar hourly_rate, bank_account
    - DELETE /api/caregivers/user_id/ → Eliminar cuidador (opcional)
    
    NO permite POST — los cuidadores se crean vía /api/auth/register/
    """
    queryset = Caregiver.objects.select_related('user').all()
    serializer_class = CaregiverSerializer
    permission_classes = [IsAuthenticated]
    
    # CRÍTICO: Como Caregiver usa user como PK, el lookup field es 'user'
    # Esto hace que las URLs sean /api/caregivers/{user_id}/
    lookup_field = 'user'
    
    # Deshabilitar el método POST (create)
    def create(self, request, *args, **kwargs):
        return Response(
            {
                'error': 'No podés crear cuidadores directamente desde este endpoint.',
                'message': 'Usá POST /api/auth/register/ con role="Caregiver"',
                'hint': 'Ejemplo: {"email": "...", "password": "...", "role": "Caregiver", "hourly_rate": "15.00"}'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    # Opcional: endpoint personalizado para buscar cuidadores verificados
    @action(detail=False, methods=['get'], url_path='verified')
    def verified_caregivers(self, request):
        """
        GET /api/caregivers/verified/
        Devuelve solo cuidadores verificados.
        """
        verified = self.queryset.filter(is_verified=True)
        serializer = self.get_serializer(verified, many=True)
        return Response(serializer.data)
    
    # Opcional: obtener el cuidador del usuario autenticado
    @action(detail=False, methods=['get'], url_path='me')
    def my_caregiver_profile(self, request):
        """
        GET /api/caregivers/me/
        Devuelve el perfil de cuidador del usuario autenticado.
        Solo funciona si el usuario es Caregiver.
        """
        if request.user.role != 'Caregiver':
            return Response(
                {'error': 'No tenés un perfil de cuidador'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            caregiver = Caregiver.objects.get(user=request.user)
            serializer = self.get_serializer(caregiver)
            return Response(serializer.data)
        except Caregiver.DoesNotExist:
            return Response(
                {'error': 'Perfil de cuidador no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )