from django.db import models
from apps.users.models import Caregiver, Admin


class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    caregiver = models.ForeignKey(Caregiver, models.DO_NOTHING, blank=True, null=True)
    file_url = models.CharField(max_length=500)
    document_type = models.TextField()
    upload_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    verification_status = models.TextField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    verified_by = models.ForeignKey(Admin, models.DO_NOTHING, db_column='verified_by', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'document'
        app_label = 'documents'  # AGREGAR ESTO