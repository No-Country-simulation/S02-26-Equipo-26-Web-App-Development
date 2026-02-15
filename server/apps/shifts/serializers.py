from rest_framework import serializers
from .models import ShiftReport


class ShiftReportSerializer(serializers.ModelSerializer):
    patient_email = serializers.CharField(source='patient.patient.email', read_only=True)
    caregiver_email = serializers.CharField(source='caregiver.caregiver.email', read_only=True)
    
    class Meta:
        model = ShiftReport
        fields = [
            'report_id', 'patient', 'patient_email', 'caregiver', 'caregiver_email',
            'payment', 'start_time', 'end_time', 'total_hours', 'report_description'
        ]