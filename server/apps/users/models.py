from django.db import models

class UserRole(models.TextChoices):
    ADMIN = "Admin", "Admin"
    CAREGIVER = "Caregiver", "Caregiver"
    PATIENT = "Patient", "Patient"


role = models.CharField(
    max_length=20,
    choices=UserRole.choices
)
