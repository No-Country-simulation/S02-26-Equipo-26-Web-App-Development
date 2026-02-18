from rest_framework import serializers
from apps.users.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer para leer y actualizar datos de Patient.
    
    IMPORTANTE: Patient usa user_id como primary key (no tiene campo 'id').
    Los campos del User son read-only porque se modifican desde /api/auth/me/update/
    """
    # La PK de Patient es user_id, no id
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'user_id',  # Este ES el ID (primary key)
            'email', 'first_name', 'last_name',
            'full_name', 'phone_number', 
            'medical_history'  # Editable
        ]
        read_only_fields = ['user_id']