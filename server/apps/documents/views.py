from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Document, DocumentStatus
from .serializers import (
    DocumentSerializer,
    DocumentCreateSerializer,
    DocumentVerificationSerializer
)


class IsAdmin(IsAuthenticated):
    """Permiso solo para admins"""
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'Admin'


class IsCaregiverOrAdmin(IsAuthenticated):
    """Permiso para caregivers (solo sus docs) o admins (todos)"""
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if request.user.role in ['Admin', 'Caregiver']:
            return True
        return False


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Documents.
    
    - GET /api/documents/ → Listar documentos (caregiver ve solo los suyos, admin ve todos)
    - POST /api/documents/ → Crear documento
    - GET /api/documents/pending/ → Documentos pendientes (solo admin)
    - POST /api/documents/{id}/approve/ → Aprobar documento (solo admin)
    - POST /api/documents/{id}/reject/ → Rechazar documento (solo admin)
    """
    queryset = Document.objects.select_related(
        'caregiver__user',
        'verified_by__user'
    ).all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DocumentCreateSerializer
        elif self.action in ['approve', 'reject']:
            return DocumentVerificationSerializer
        return DocumentSerializer
    
    def get_permissions(self):
        if self.action in ['approve', 'reject', 'pending']:
            return [IsAdmin()]
        return [IsCaregiverOrAdmin()]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Si es caregiver, solo ve sus documentos
        if user.role == 'Caregiver':
            try:
                caregiver = user.caregiver_profile
                queryset = queryset.filter(caregiver=caregiver)
            except:
                queryset = queryset.none()
        
        # Filtros opcionales
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(verification_status=status_filter)
        
        doc_type = self.request.query_params.get('type')
        if doc_type:
            queryset = queryset.filter(document_type=doc_type)
        
        return queryset.order_by('-upload_date')
    
    def perform_create(self, serializer):
        """Asignar automáticamente el caregiver si es cuidador creando su doc"""
        user = self.request.user
        
        if user.role == 'Caregiver':
            # El cuidador crea su propio documento
            caregiver = user.caregiver_profile
            serializer.save(caregiver=caregiver)
        else:
            # Admin crea documento para un cuidador específico
            serializer.save()
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdmin])
    def pending(self, request):
        """
        GET /api/documents/pending/
        Documentos pendientes de verificación.
        """
        queryset = self.get_queryset().filter(verification_status=DocumentStatus.PENDING)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = DocumentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = DocumentSerializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def approve(self, request, pk=None):
        """
        POST /api/documents/{id}/approve/
        Aprobar un documento.
        """
        document = self.get_object()
        
        if document.verification_status == DocumentStatus.APPROVED:
            return Response(
                {'message': 'El documento ya está aprobado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(document, data={
            'verification_status': DocumentStatus.APPROVED,
            'rejection_reason': ''
        }, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Guardar quién aprobó
        from apps.users.models import Admin
        try:
            admin_profile = Admin.objects.get(user=request.user)
            serializer.save(verified_by=admin_profile)
        except Admin.DoesNotExist:
            return Response(
                {'error': 'No se encontró perfil de administrador'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'message': 'Documento aprobado exitosamente',
            'document': DocumentSerializer(document).data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def reject(self, request, pk=None):
        """
        POST /api/documents/{id}/reject/
        Rechazar un documento.
        """
        document = self.get_object()
        
        if document.verification_status == DocumentStatus.REJECTED:
            return Response(
                {'message': 'El documento ya está rechazado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(document, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Asegurar que se marca como rechazado
        serializer.validated_data['verification_status'] = DocumentStatus.REJECTED
        
        # Guardar quién rechazó
        from apps.users.models import Admin
        try:
            admin_profile = Admin.objects.get(user=request.user)
            serializer.save(verified_by=admin_profile)
        except Admin.DoesNotExist:
            return Response(
                {'error': 'No se encontró perfil de administrador'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'message': 'Documento rechazado',
            'document': DocumentSerializer(document).data
        })