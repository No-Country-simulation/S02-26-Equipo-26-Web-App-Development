from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer


class IsAdmin(IsAuthenticated):
    """Permiso: solo admins"""
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view) and 
            request.user.role == 'Admin'
        )


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Payments.
    Solo accesible por admins.
    
    Endpoints:
    - GET /api/payments/ → Listar todos los pagos
    - GET /api/payments/?caregiver_id=2 → Pagos de un cuidador
    - GET /api/payments/?status=Success → Filtrar por estado
    - GET /api/payments/{id}/ → Detalle de un pago
    - POST /api/payments/ → Crear pago
    - PATCH /api/payments/{id}/ → Actualizar pago
    - DELETE /api/payments/{id}/ → Eliminar pago
    """
    queryset = Payment.objects.select_related('caregiver__user').all()
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer
    
    def get_queryset(self):
        """Filtros disponibles"""
        queryset = super().get_queryset()
        
        # Filtrar por cuidador
        caregiver_id = self.request.query_params.get('caregiver_id')
        if caregiver_id:
            queryset = queryset.filter(caregiver__user_id=caregiver_id)
        
        # Filtrar por estado
        payment_status = self.request.query_params.get('status')
        if payment_status:
            queryset = queryset.filter(status=payment_status)
        
        return queryset.order_by('-payment_date')