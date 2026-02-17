from django.db import models
from apps.patients.models import Patient
from apps.caregivers.models import Caregiver
from apps.payments.models import Payment


class ShiftReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='shift_reports')
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE, related_name='shift_reports')
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='shift_reports'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    report_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'shift_report'
        verbose_name = 'Shift Report'
        verbose_name_plural = 'Shift Reports'

    def __str__(self):
        return f"Shift {self.id} - {self.caregiver.user.full_name}"

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            self.total_hours = round(duration.total_seconds() / 3600, 2)
        super().save(*args, **kwargs)