from django.db import models


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'location'
        app_label = 'users'


class User(models.Model):
    # Requeridos por Django cuando AUTH_USER_MODEL apunta a este modelo
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]

    user_id = models.AutoField(primary_key=True)
    location = models.ForeignKey(Location, models.DO_NOTHING, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=225)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.TextField()  # TODO: Cambiar a choices con los ENUM
    address_line = models.CharField(max_length=225, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Admin(models.Model):
    admin = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    access_level = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin'


class Patient(models.Model):
    patient = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    medical_history = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient'


class Caregiver(models.Model):
    caregiver = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bank_account = models.CharField(max_length=25, blank=True, null=True)
    is_verified = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'caregiver'


class Family(models.Model):
    family_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, models.DO_NOTHING, blank=True, null=True)
    relationship = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'family'