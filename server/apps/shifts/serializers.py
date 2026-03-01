from rest_framework import serializers
from .models import ShiftReport


class ShiftReportSerializer(serializers.ModelSerializer):
    caregiver_id = serializers.IntegerField(source='caregiver.user_id', read_only=True)
    caregiver_name = serializers.CharField(source='caregiver.user.full_name', read_only=True)
    patient_id = serializers.IntegerField(source='patient.user_id', read_only=True)
    patient_name = serializers.CharField(source='patient.user.full_name', read_only=True)
    is_paid = serializers.SerializerMethodField()
    
    class Meta:
        model = ShiftReport
        fields = [
            'id', 'assignment', 'caregiver_id', 'caregiver_name',
            'patient_id', 'patient_name', 'start_time', 'end_time',
            'total_hours', 'status', 'important_notes', 'tasks_performed',
            'patient_signature', 'confirmed_at', 'payment', 'is_paid', 'created_at'
        ]
        read_only_fields = ['id', 'total_hours', 'created_at']
    
    def get_is_paid(self, obj):
        return obj.payment is not None


class ShiftReportCreateSerializer(serializers.ModelSerializer):
    caregiver_id = serializers.IntegerField(write_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ShiftReport
        fields = [
            'caregiver_id', 'patient_id', 'start_time', 'end_time',
            'status', 'important_notes', 'tasks_performed', 'patient_signature'
        ]
    
    def validate(self, data):
        from apps.caregivers.models import Caregiver
        from apps.patients.models import Patient
        
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
        
        if data.get('end_time') and data['start_time']:
            if data['end_time'] <= data['start_time']:
                raise serializers.ValidationError({'end_time': 'Debe ser posterior a start_time'})
        
        return data
    
    def create(self, validated_data):
        caregiver = validated_data.pop('caregiver')
        patient = validated_data.pop('patient')
        validated_data.pop('caregiver_id', None)
        validated_data.pop('patient_id', None)
        
        return ShiftReport.objects.create(
            caregiver=caregiver,
            patient=patient,
            **validated_data
        )