from django.db import models
from django.conf import settings


class Admin(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='admin_profile'
    )
    access_level = models.IntegerField(default=1)

    class Meta:
        db_table = 'admin'
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

    def __str__(self):
        return f"Admin: {self.user.full_name}"