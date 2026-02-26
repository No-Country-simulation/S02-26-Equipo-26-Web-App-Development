from django.db import models


class PaymentStatus(models.TextChoices):
    PENDING = 'Pending', 'Pendiente'
    SUCCESS = 'Success', 'Exitoso'
    FAILED = 'Failed', 'Fallido'


class Payment(models.Model):
    caregiver = models.ForeignKey(
        'caregivers.Caregiver',
        on_delete=models.CASCADE,
        related_name='payments'
    )
    period_start = models.DateField(help_text="Inicio del período de pago")
    period_end = models.DateField(help_text="Fin del período de pago")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    payment_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'payment'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-payment_date']

    def __str__(self):
        return f"Payment {self.id} - ${self.total_amount} to {self.caregiver.user.full_name}"