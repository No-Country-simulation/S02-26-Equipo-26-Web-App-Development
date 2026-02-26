from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Assignment
from .serializers import (
    AssignmentSerializer,
    AssignmentCreateSerializer,
    AssignmentUpdateSerializer
)


class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'Admin'


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de asignaciones cuidador-paciente.
    Solo accesible por admins.
    
    Endpoints:
    - GET /api/assignments/ → Listar todas las asignaciones
    - GET /api/assignments/?status=Active → Filtrar por estado
    - GET /api/assignments/?caregiver_id=2 → Asignaciones de un cuidador
    - GET /api/assignments/?patient_id=1 → Asignaciones de un paciente
    - GET /api/assignments/{id}/ → Detalle de una asignación
    - POST /api/assignments/ → Crear asignación
    - PATCH /api/assignments/{id}/ → Actualizar asignación
    - DELETE /api/assignments/{id}/ → Eliminar asignación
    - POST /api/assignments/{id}/complete/ → Marcar como completada
    - POST /api/assignments/{id}/cancel/ → Cancelar asignación
    - GET /api/assignments/active/ → Solo asignaciones activas
    """
    queryset = Assignment.objects.select_related(
        'caregiver__user',
        'patient__user',
        'assigned_by__user'
    ).all()
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AssignmentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AssignmentUpdateSerializer
        return AssignmentSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        assignment_status = self.request.query_params.get('status')
        if assignment_status:
            queryset = queryset.filter(status=assignment_status)
        
        caregiver_id = self.request.query_params.get('caregiver_id')
        if caregiver_id:
            queryset = queryset.filter(caregiver__user_id=caregiver_id)
        
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient__user_id=patient_id)
        
        return queryset.order_by('-start_date')
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        GET /api/assignments/active/
        Devuelve solo asignaciones activas.
        """
        from datetime import date
        active_assignments = self.get_queryset().filter(
            status='Active'
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=date.today())
        )
        
        serializer = self.get_serializer(active_assignments, many=True)
        return Response({
            'count': active_assignments.count(),
            'results': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        POST /api/assignments/{id}/complete/
        Marca la asignación como completada.
        """
        assignment = self.get_object()
        
        if assignment.status == 'Completed':
            return Response(
                {'message': 'La asignación ya está completada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        assignment.status = 'Completed'
        assignment.save()
        
        serializer = self.get_serializer(assignment)
        return Response({
            'message': 'Asignación marcada como completada',
            'assignment': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        POST /api/assignments/{id}/cancel/
        Cancela la asignación.
        """
        assignment = self.get_object()
        
        if assignment.status == 'Cancelled':
            return Response(
                {'message': 'La asignación ya está cancelada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        assignment.status = 'Cancelled'
        assignment.save()
        
        serializer = self.get_serializer(assignment)
        return Response({
            'message': 'Asignación cancelada',
            'assignment': serializer.data
        })