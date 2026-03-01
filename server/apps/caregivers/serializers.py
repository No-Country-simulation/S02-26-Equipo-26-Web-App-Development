# server/apps/caregivers/serializers.py
from rest_framework import serializers
from .models import Caregiver, Specialty


# ========== TUS SERIALIZERS EXISTENTES (SIN TOCAR) ==========

class CaregiverSerializer(serializers.ModelSerializer):
    """
    Serializer para leer y actualizar datos de Caregiver.
    
    IMPORTANTE: Caregiver usa user_id como primary key (no tiene campo 'id').
    Los campos del User son read-only porque se modifican desde /api/auth/me/update/
    """
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Caregiver
        fields = [
            'user_id',
            'email', 'first_name', 'last_name',
            'full_name', 'phone_number', 
            'hourly_rate',
            'bank_account',
            'is_verified'
        ]
        read_only_fields = ['user_id', 'is_verified']


# ========== NUEVOS SERIALIZERS PARA ADMIN ==========

class SpecialtySerializer(serializers.ModelSerializer):
    """Para listar especialidades"""
    class Meta:
        model = Specialty
        fields = ['id', 'name', 'description']


class CaregiverListSerializer(serializers.ModelSerializer):
    """
    Para listar cuidadores en el dashboard del admin.
    Incluye specialty y datos del usuario.
    """
    id = serializers.IntegerField(source='user.id', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)
    specialty_name = serializers.CharField(source='specialty.name', read_only=True)
    
    class Meta:
        model = Caregiver
        fields = [
            'id', 'full_name', 'email', 'phone_number',
            'specialty', 'specialty_name', 'hourly_rate',
            'is_verified', 'is_active', 'bank_account'
        ]


class CaregiverCreateSerializer(serializers.Serializer):
    """
    Para que Admin cree nuevos cuidadores.
    No es ModelSerializer porque crea User + Caregiver.
    """
    # Datos de usuario
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, min_length=6)
    
    # Datos de cuidador
    hourly_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    specialty_id = serializers.IntegerField(required=False, allow_null=True)
    bank_account = serializers.CharField(max_length=25, required=False, allow_blank=True)
    
    def validate_email(self, value):
        from apps.users.models import User
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado")
        return value
    
    def validate_specialty_id(self, value):
        if value and not Specialty.objects.filter(id=value).exists():
            raise serializers.ValidationError("Especialidad no válida")
        return value


class CaregiverDetailSerializer(serializers.ModelSerializer):
    """
    Para ver detalle completo de un cuidador.
    """
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)
    specialty_detail = SpecialtySerializer(source='specialty', read_only=True)
    
    class Meta:
        model = Caregiver
        fields = [
            'user_id', 'full_name', 'email', 'phone_number',
            'specialty', 'specialty_detail', 'hourly_rate',
            'bank_account', 'is_verified', 'is_active'
        ]