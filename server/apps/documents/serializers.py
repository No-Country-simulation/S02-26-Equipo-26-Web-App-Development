from rest_framework import serializers
from apps.users.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    caregiver_name = serializers.CharField(source='caregiver.user.full_name', read_only=True)
    caregiver_email = serializers.CharField(source='caregiver.user.email', read_only=True)
    verified_by_name = serializers.CharField(source='verified_by.user.full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = Document
        fields = [
            'id', 'caregiver', 'caregiver_name', 'caregiver_email',
            'file_url', 'document_type', 'upload_date', 'expiry_date',
            'verification_status', 'rejection_reason', 'verified_by', 'verified_by_name'
        ]
        read_only_fields = ['id', 'upload_date']