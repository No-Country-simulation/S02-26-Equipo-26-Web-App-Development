from django.db import models
from apps.users.models import Patient, Caregiver
from apps.payments.models import Payment


class ShiftReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, models.DO_NOTHING, blank=True, null=True)
    caregiver = models.ForeignKey(Caregiver, models.DO_NOTHING, blank=True, null=True)
    payment = models.ForeignKey(Payment, models.DO_NOTHING, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    report_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shift_report'
        app_label = 'shifts'  # AGREGAR ESTO