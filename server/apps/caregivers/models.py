from django.db import models
from django.conf import settings


class Caregiver(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='caregiver_profile'
    )
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bank_account = models.CharField(max_length=25, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'caregiver'
        verbose_name = 'Caregiver'
        verbose_name_plural = 'Caregivers'

    def __str__(self):
        return f"Caregiver: {self.user.full_name}"