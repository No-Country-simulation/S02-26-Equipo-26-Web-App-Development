from django.db import models
from apps.caregivers.models import Caregiver


class DocumentType(models.TextChoices):
    ID_CARD = 'ID_card', 'ID Card'
    CRIMINAL_RECORD = 'Criminal_record', 'Criminal Record'
    CERTIFICATION = 'Certification', 'Certification'
    INSURANCE = 'Insurance', 'Insurance'


class DocumentStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    APPROVED = 'Approved', 'Approved'
    REJECTED = 'Rejected', 'Rejected'


class Document(models.Model):
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE, related_name='documents')
    file_url = models.URLField(max_length=500)
    document_type = models.CharField(max_length=20, choices=DocumentType.choices)
    upload_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    verification_status = models.CharField(
        max_length=20, choices=DocumentStatus.choices, default=DocumentStatus.PENDING
    )
    rejection_reason = models.TextField(blank=True, null=True)
    # String reference para evitar import circular con una app 'admins' si la crearas
    verified_by = models.ForeignKey(
        'admins.Admin', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='verified_documents'
    )

    class Meta:
        db_table = 'document'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return f"{self.document_type} - {self.caregiver.user.full_name}"