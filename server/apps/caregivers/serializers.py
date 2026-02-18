from rest_framework import serializers
from apps.users.models import Caregiver


class CaregiverSerializer(serializers.ModelSerializer):
    """
    Serializer para leer y actualizar datos de Caregiver.
    
    IMPORTANTE: Caregiver usa user_id como primary key (no tiene campo 'id').
    Los campos del User son read-only porque se modifican desde /api/auth/me/update/
    """
    # La PK de Caregiver es user_id, no id
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Caregiver
        fields = [
            'user_id',  # Este ES el ID (primary key)
            'email', 'first_name', 'last_name',
            'full_name', 'phone_number', 
            'hourly_rate',  # Editable
            'bank_account',  # Editable
            'is_verified'  # Read-only (solo admins lo cambian)
        ]
        read_only_fields = ['user_id', 'is_verified']