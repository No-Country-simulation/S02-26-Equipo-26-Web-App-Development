#from django.db import models

# El modelo Patient está en apps.users.models




from django.db import models

from apps.users.models import User


class Patient(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='patient_profile',
    )
    medical_history = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'patient'
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def __str__(self):
        return f"Patient: {self.user.full_name}"


class Family(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='family_members',
    )
    relationship = models.CharField(max_length=50)

    class Meta:
        db_table = 'family'
        verbose_name = 'Family Member'
        verbose_name_plural = 'Family Members'

    def __str__(self):
        return f"{self.relationship} of {self.patient.user.full_name}"
