from django.db import models
from apps.users.models import Caregiver


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    caregiver = models.ForeignKey(Caregiver, models.DO_NOTHING, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(unique=True, max_length=255, blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment'
        app_label = 'payments'  # AGREGAR ESTO