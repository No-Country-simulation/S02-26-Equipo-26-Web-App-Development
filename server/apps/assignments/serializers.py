from rest_framework import serializers
from .models import Assignment
from apps.caregivers.models import Caregiver
from apps.patients.models import Patient
from apps.users.models import Admin


class AssignmentSerializer(serializers.ModelSerializer):
    caregiver_id = serializers.IntegerField(source='caregiver.user_id', read_only=True)
    caregiver_name = serializers.CharField(source='caregiver.user.full_name', read_only=True)
    patient_id = serializers.IntegerField(source='patient.user_id', read_only=True)
    patient_name = serializers.CharField(source='patient.user.full_name', read_only=True)
    assigned_by_name = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Assignment
        fields = [
            'id',
            'caregiver_id',
            'caregiver_name',
            'patient_id',
            'patient_name',
            'assigned_by',
            'assigned_by_name',
            'start_date',
            'end_date',
            'care_type',
            'status',
            'is_active',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_assigned_by_name(self, obj):
        if obj.assigned_by:
            return obj.assigned_by.user.full_name
        return None


class AssignmentCreateSerializer(serializers.ModelSerializer):
    caregiver_id = serializers.IntegerField(write_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Assignment
        fields = [
            'caregiver_id',
            'patient_id',
            'start_date',
            'end_date',
            'care_type',
            'status'
        ]
    
    def validate(self, data):
        try:
            caregiver = Caregiver.objects.get(user_id=data['caregiver_id'])
            data['caregiver'] = caregiver
        except Caregiver.DoesNotExist:
            raise serializers.ValidationError({'caregiver_id': 'Cuidador no encontrado'})
        
        try:
            patient = Patient.objects.get(user_id=data['patient_id'])
            data['patient'] = patient
        except Patient.DoesNotExist:
            raise serializers.ValidationError({'patient_id': 'Paciente no encontrado'})
        
        if data.get('end_date') and data['start_date']:
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError({'end_date': 'end_date debe ser posterior a start_date'})
        
        return data
    
    def create(self, validated_data):
        caregiver = validated_data.pop('caregiver')
        patient = validated_data.pop('patient')
        validated_data.pop('caregiver_id', None)
        validated_data.pop('patient_id', None)
        
        user = self.context['request'].user
        try:
            admin_profile = Admin.objects.get(user=user)
            validated_data['assigned_by'] = admin_profile
        except Admin.DoesNotExist:
            pass
        
        assignment = Assignment.objects.create(
            caregiver=caregiver,
            patient=patient,
            **validated_data
        )
        return assignment


class AssignmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['end_date', 'care_type', 'status']
    
    def validate(self, data):
        if data.get('end_date') and self.instance.start_date:
            if data['end_date'] < self.instance.start_date:
                raise serializers.ValidationError({'end_date': 'end_date debe ser posterior a start_date'})
        return data