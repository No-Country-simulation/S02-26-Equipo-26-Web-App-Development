from rest_framework import serializers
from .models import Location, User, Admin, Caregiver, Patient, Family


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['location_id', 'country', 'city']


class UserSerializer(serializers.ModelSerializer):
    location_details = LocationSerializer(source='location', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name', 'email', 
            'phone_number', 'role', 'address_line', 'is_active',
            'location', 'location_details', 'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']


class AdminSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='admin', read_only=True)
    
    class Meta:
        model = Admin
        fields = ['admin', 'access_level', 'user_details']


class CaregiverSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='caregiver', read_only=True)
    
    class Meta:
        model = Caregiver
        fields = [
            'caregiver', 'hourly_rate', 'bank_account', 
            'is_verified', 'user_details'
        ]


class PatientSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='patient', read_only=True)
    
    class Meta:
        model = Patient
        fields = ['patient', 'medical_history', 'user_details']


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ['family_id', 'patient', 'relationship']