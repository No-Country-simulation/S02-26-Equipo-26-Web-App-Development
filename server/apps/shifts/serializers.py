from rest_framework import serializers
from apps.users.models import ShiftReport


class ShiftReportSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.full_name', read_only=True)
    caregiver_name = serializers.CharField(source='caregiver.user.full_name', read_only=True)
    
    class Meta:
        model = ShiftReport
        fields = [
            'id', 'patient', 'patient_name', 'caregiver', 'caregiver_name',
            'payment', 'start_time', 'end_time', 'total_hours', 'report_description'
        ]
        read_only_fields = ['id', 'total_hours']