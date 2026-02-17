from django.db import models
from apps.caregivers.models import Caregiver


class PaymentStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    SUCCESS = 'Success', 'Success'
    FAILED = 'Failed', 'Failed'


class Payment(models.Model):
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'payment'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f"Payment {self.id} - {self.caregiver.user.full_name}"