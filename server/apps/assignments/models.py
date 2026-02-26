from django.db import models
from django.core.exceptions import ValidationError


class AssignmentStatus(models.TextChoices):
    ACTIVE = 'Active', 'Activa'
    COMPLETED = 'Completed', 'Finalizada'
    CANCELLED = 'Cancelled', 'Cancelada'
    ON_HOLD = 'OnHold', 'En Pausa'


class CareType(models.TextChoices):
    FULL_TIME = 'FullTime', 'Tiempo Completo'
    PART_TIME = 'PartTime', 'Medio Tiempo'
    HOURLY = 'Hourly', 'Por Horas'
    LIVE_IN = 'LiveIn', 'Cama Adentro'
    OVERNIGHT = 'Overnight', 'Nocturno'


class Assignment(models.Model):
    caregiver = models.ForeignKey('caregivers.Caregiver', on_delete=models.CASCADE, related_name='assignments')
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='assignments')
    assigned_by = models.ForeignKey('users.Admin', on_delete=models.SET_NULL, null=True, blank=True, related_name='assignments_created', db_column='assigned_by_id')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    care_type = models.CharField(max_length=20, choices=CareType.choices, default=CareType.FULL_TIME)
    status = models.CharField(max_length=20, choices=AssignmentStatus.choices, default=AssignmentStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'assignments'
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
        ordering = ['-start_date']

    def __str__(self):
        caregiver_name = self.caregiver.user.full_name
        patient_name = self.patient.user.full_name
        return f"{caregiver_name} -> {patient_name} ({self.status})"

    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError('end_date debe ser posterior a start_date')

    @property
    def is_active(self):
        from datetime import date
        today = date.today()
        is_status_active = self.status == AssignmentStatus.ACTIVE
        is_date_valid = self.end_date is None or self.end_date >= today
        return is_status_active and is_date_valid