from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Location, Patient, Caregiver, Admin


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'country', 'city']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    location_id = serializers.IntegerField(required=False, allow_null=True)

    # Campos adicionales según el rol
    medical_history = serializers.CharField(required=False, allow_blank=True)
    hourly_rate = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    bank_account = serializers.CharField(max_length=25, required=False, allow_blank=True)
    access_level = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm', 'first_name', 'last_name',
            'phone_number', 'role', 'address_line', 'location_id',
            # Campos específicos por rol
            'medical_history', 'hourly_rate', 'bank_account', 'access_level'
        ]

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden"})
        
        role = attrs.get('role')
        
        # Validaciones específicas por rol
        if role == 'Caregiver':
            if not attrs.get('hourly_rate'):
                raise serializers.ValidationError({"hourly_rate": "Tarifa por hora requerida para cuidadores"})
        
        return attrs

    def create(self, validated_data):
        # Remover campos que no pertenecen al modelo User
        validated_data.pop('password_confirm')
        medical_history = validated_data.pop('medical_history', None)
        hourly_rate = validated_data.pop('hourly_rate', None)
        bank_account = validated_data.pop('bank_account', None)
        access_level = validated_data.pop('access_level', None)
        location_id = validated_data.pop('location_id', None)

        # Obtener ubicación si existe
        if location_id:
            try:
                location = Location.objects.get(id=location_id)
                validated_data['location'] = location
            except Location.DoesNotExist:
                pass

        # Crear usuario base
        user = User.objects.create_user(**validated_data)

        # Crear perfil según el rol
        role = user.role
        if role == 'Patient':
            Patient.objects.create(user=user, medical_history=medical_history or '')
        elif role == 'Caregiver':
            Caregiver.objects.create(
                user=user,
                hourly_rate=hourly_rate,
                bank_account=bank_account or ''
            )
        elif role == 'Admin':
            Admin.objects.create(user=user, access_level=access_level or 1)

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['medical_history']


class CaregiverProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caregiver
        fields = ['hourly_rate', 'bank_account', 'is_verified']


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['access_level']


class UserDetailSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    patient_profile = PatientProfileSerializer(read_only=True)
    caregiver_profile = CaregiverProfileSerializer(read_only=True)
    admin_profile = AdminProfileSerializer(read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number', 'role', 'address_line', 'is_active',
            'created_at', 'location',
            'patient_profile', 'caregiver_profile', 'admin_profile'
        ]
        read_only_fields = ['id', 'created_at', 'is_active']
