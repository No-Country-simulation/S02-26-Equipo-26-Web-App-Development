from rest_framework import serializers
from .models import Document, DocumentStatus, DocumentType


class DocumentSerializer(serializers.ModelSerializer):
    caregiver_name = serializers.CharField(source='caregiver.user.full_name', read_only=True)
    caregiver_email = serializers.CharField(source='caregiver.user.email', read_only=True)
    verified_by_name = serializers.CharField(
        source='verified_by.user.full_name',
        read_only=True,
        allow_null=True,
    )
    document_type_display = serializers.CharField(
        source='get_document_type_display',
        read_only=True
    )
    verification_status_display = serializers.CharField(
        source='get_verification_status_display',
        read_only=True
    )
    
    class Meta:
        model = Document
        fields = [
            'id', 'caregiver', 'caregiver_name', 'caregiver_email',
            'file_url', 'document_type', 'document_type_display',
            'upload_date', 'expiry_date',
            'verification_status', 'verification_status_display',
            'rejection_reason', 'verified_by', 'verified_by_name'
        ]
        read_only_fields = ['id', 'upload_date', 'verification_status', 'verified_by', 'rejection_reason']


class DocumentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear documentos.
    - Cuidador: caregiver se asigna automáticamente (no enviar en JSON)
    - Admin: puede enviar caregiver_id para crear doc en nombre de otro
    """
    # Campo opcional solo para admin
    caregiver_id = serializers.IntegerField(required=False, write_only=True)
    
    class Meta:
        model = Document
        fields = ['caregiver_id', 'file_url', 'document_type', 'expiry_date']
    
    def validate_document_type(self, value):
        valid_types = [choice[0] for choice in DocumentType.choices]
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Tipo inválido. Opciones: {', '.join(valid_types)}"
            )
        return value
    
    def validate(self, data):
        """
        Validar que admin envía caregiver_id si es admin.
        Cuidador no necesita enviarlo (se asigna en el view).
        """
        request = self.context.get('request')
        if request and request.user.role == 'Admin':
            if 'caregiver_id' not in data:
                raise serializers.ValidationError({
                    'caregiver_id': 'El admin debe especificar el caregiver_id'
                })
        return data


class DocumentVerificationSerializer(serializers.ModelSerializer):
    """
    Serializer para que admins aprueben/rechacen documentos.
    """
    rejection_reason = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Document
        fields = ['verification_status', 'rejection_reason']
    
    def validate(self, data):
        status = data.get('verification_status')
        reason = data.get('rejection_reason', '')
        
        if status == DocumentStatus.REJECTED and not reason:
            raise serializers.ValidationError({
                'rejection_reason': 'Debe proporcionar un motivo de rechazo'
            })
        
        # Limpiar razón si se aprueba
        if status == DocumentStatus.APPROVED:
            data['rejection_reason'] = ''
        
        return data