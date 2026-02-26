from rest_framework import serializers
from apps.shifts.models import ShiftReport
from apps.patients.models import Patient
from apps.caregivers.models import Caregiver
from apps.assignments.models import Assignment
from datetime import datetime


class ShiftReportSerializer(serializers.ModelSerializer):
    """
    Serializer completo para leer turnos.
    """
    # Info del cuidador
    caregiver_id = serializers.IntegerField(source='caregiver.user_id', read_only=True)
    caregiver_name = serializers.CharField(source='caregiver.user.full_name', read_only=True)
    caregiver_email = serializers.CharField(source='caregiver.user.email', read_only=True)
    
    # Info del paciente
    patient_id = serializers.IntegerField(source='patient.user_id', read_only=True)
    patient_name = serializers.CharField(source='patient.user.full_name', read_only=True)
    
    # Info de la asignación
    assignment_id = serializers.IntegerField(source='assignment.id', read_only=True)
    
    # Campos calculados
    duration_hours = serializers.SerializerMethodField()
    is_paid = serializers.SerializerMethodField()
    
    class Meta:
        model = ShiftReport
        fields = [
            'id',
            'assignment_id',
            'caregiver_id',
            'caregiver_name',
            'caregiver_email',
            'patient_id',
            'patient_name',
            'start_time',
            'end_time',
            'total_hours',
            'duration_hours',
            'status',
            'important_notes',
            'tasks_performed',
            'patient_signature',
            'confirmed_at',
            'payment',
            'is_paid',
            'created_at'
        ]
        read_only_fields = ['id', 'total_hours', 'created_at']
    
    def get_duration_hours(self, obj):
        return obj.total_hours
    
    def get_is_paid(self, obj):
        return obj.payment is not None and obj.payment.status == 'Success'


class ShiftReportCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear turnos.
    Acepta caregiver_id y patient_id, valida que exista asignación activa.
    """
    caregiver_id = serializers.IntegerField(write_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ShiftReport
        fields = [
            'caregiver_id',
            'patient_id',
            'start_time',
            'end_time',
            'status',
            'important_notes',
            'tasks_performed',
            'patient_signature',
        ]
    
    def validate(self, data):
        """Validaciones"""
        # Verificar que el cuidador existe
        try:
            caregiver = Caregiver.objects.get(user_id=data['caregiver_id'])
            data['caregiver'] = caregiver
        except Caregiver.DoesNotExist:
            raise serializers.ValidationError({
                'caregiver_id': 'Cuidador no encontrado'
            })
        
        # Verificar que el paciente existe
        try:
            patient = Patient.objects.get(user_id=data['patient_id'])
            data['patient'] = patient
        except Patient.DoesNotExist:
            raise serializers.ValidationError({
                'patient_id': 'Paciente no encontrado'
            })
        
        # Buscar asignación activa
        from django.db.models import Q
        assignment = Assignment.objects.filter(
            caregiver=caregiver,
            patient=patient,
            status='Active',
            start_date__lte=data['start_time'].date()
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=data['start_time'].date())
        ).first()
        
        if not assignment:
            raise serializers.ValidationError(
                'No existe una asignación activa entre este cuidador y paciente. '
                'Creá una asignación primero desde /api/assignments/'
            )
        
        data['assignment'] = assignment
        
        # Validar fechas
        if data.get('end_time') and data['start_time']:
            if data['end_time'] <= data['start_time']:
                raise serializers.ValidationError({
                    'end_time': 'end_time debe ser posterior a start_time'
                })
        
        return data
    
    def create(self, validated_data):
        # Extraer los objetos y remover los IDs
        caregiver = validated_data.pop('caregiver')
        patient = validated_data.pop('patient')
        assignment = validated_data.pop('assignment')
        validated_data.pop('caregiver_id', None)
        validated_data.pop('patient_id', None)
        
        # Crear el turno
        shift = ShiftReport.objects.create(
            assignment=assignment,
            caregiver=caregiver,
            patient=patient,
            **validated_data
        )
        return shift


class ShiftReportUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar turnos existentes.
    """
    class Meta:
        model = ShiftReport
        fields = [
            'end_time',
            'status',
            'important_notes',
            'tasks_performed',
            'patient_signature',
            'confirmed_at',
        ]
    
    def validate(self, data):
        """Validar fechas si se están actualizando"""
        start = self.instance.start_time
        end = data.get('end_time', self.instance.end_time)
        
        if end and start and end <= start:
            raise serializers.ValidationError({
                'end_time': 'end_time debe ser posterior a start_time'
            })
        
        return data


class HoursSummarySerializer(serializers.Serializer):
    """
    Serializer para el resumen de horas trabajadas.
    """
    caregiver_id = serializers.IntegerField()
    caregiver_name = serializers.CharField()
    caregiver_email = serializers.CharField()
    total_hours = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_shifts = serializers.IntegerField()
    paid_hours = serializers.DecimalField(max_digits=10, decimal_places=2)
    unpaid_hours = serializers.DecimalField(max_digits=10, decimal_places=2)
    hourly_rate = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    amount_due = serializers.DecimalField(max_digits=10, decimal_places=2)