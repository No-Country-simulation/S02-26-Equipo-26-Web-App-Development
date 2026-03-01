# server/apps/caregivers/models.py
from django.db import models
from apps.users.models import User


class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'specialty'
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Caregiver(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='caregiver_profile',
    )
    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    bank_account = models.CharField(max_length=25, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='caregivers'
    )

    class Meta:
        db_table = 'caregiver'
        verbose_name = 'Caregiver'
        verbose_name_plural = 'Caregivers'

    def __str__(self):
        return f"Caregiver: {self.user.full_name}"