from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    caregiver_email = serializers.CharField(source='caregiver.caregiver.email', read_only=True)
    verified_by_email = serializers.CharField(source='verified_by.admin.email', read_only=True, allow_null=True)
    
    class Meta:
        model = Document
        fields = [
            'document_id', 'caregiver', 'caregiver_email', 'file_url',
            'document_type', 'upload_date', 'expiry_date',
            'verification_status', 'rejection_reason', 'verified_by', 'verified_by_email'
        ]