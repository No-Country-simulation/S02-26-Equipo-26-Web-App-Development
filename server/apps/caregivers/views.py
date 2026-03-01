# server/apps/caregivers/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction

from .models import Caregiver, Specialty
from .serializers import (
    CaregiverListSerializer,
    CaregiverDetailSerializer,
    CaregiverCreateSerializer,
    SpecialtySerializer
)
from apps.users.models import User


class SpecialtyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar especialidades.
    GET /api/caregivers/specialties/
    """
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [IsAuthenticated]


class CaregiverViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Caregivers.
    """
    queryset = Caregiver.objects.select_related('user', 'specialty').all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'user'
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CaregiverCreateSerializer
        elif self.action == 'list':
            return CaregiverListSerializer
        return CaregiverDetailSerializer
    
    def get_permissions(self):
        # Solo admins pueden crear cuidadores
        if self.action == 'create':
            return [IsAuthenticated()]
        return super().get_permissions()
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        POST /api/caregivers/
        Crea un nuevo cuidador (solo Admin).
        """
        # Verificar que sea admin
        if request.user.role != 'Admin':
            return Response(
                {'error': 'Solo administradores pueden crear cuidadores'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        # Crear usuario
        user = User.objects.create_user(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data.get('phone_number', ''),
            role='Caregiver'
        )
        
        # Crear perfil de cuidador
        caregiver = Caregiver.objects.create(
            user=user,
            hourly_rate=data['hourly_rate'],
            specialty_id=data.get('specialty_id'),
            bank_account=data.get('bank_account', '')
        )
        
        return Response({
            'success': True,
            'message': 'Cuidador creado exitosamente',
            'data': {
                'id': user.id,
                'full_name': user.full_name,
                'email': user.email,
                'specialty': caregiver.specialty.name if caregiver.specialty else None,
                'hourly_rate': str(caregiver.hourly_rate)
            }
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], url_path='specialties')
    def list_specialties(self, request):
        """
        GET /api/caregivers/specialties/
        Lista todas las especialidades disponibles.
        """
        specialties = Specialty.objects.all()
        serializer = SpecialtySerializer(specialties, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='verified')
    def verified_caregivers(self, request):
        verified = self.queryset.filter(is_verified=True)
        serializer = CaregiverListSerializer(verified, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='me')
    def my_caregiver_profile(self, request):
        if request.user.role != 'Caregiver':
            return Response(
                {'error': 'No tenés un perfil de cuidador'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            caregiver = Caregiver.objects.get(user=request.user)
            serializer = CaregiverDetailSerializer(caregiver)
            return Response(serializer.data)
        except Caregiver.DoesNotExist:
            return Response(
                {'error': 'Perfil de cuidador no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )