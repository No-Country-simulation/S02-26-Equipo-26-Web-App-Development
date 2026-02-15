# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    admin = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)
    access_level = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin'


class Caregiver(models.Model):
    caregiver = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bank_account = models.CharField(max_length=25, blank=True, null=True)
    is_verified = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'caregiver'


class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    caregiver = models.ForeignKey(Caregiver, models.DO_NOTHING, blank=True, null=True)
    file_url = models.CharField(max_length=500)
    document_type = models.TextField()  # This field type is a guess.
    upload_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    verification_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    rejection_reason = models.TextField(blank=True, null=True)
    verified_by = models.ForeignKey(Admin, models.DO_NOTHING, db_column='verified_by', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'document'


class Family(models.Model):
    family_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey('Patient', models.DO_NOTHING, blank=True, null=True)
    relationship = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'family'


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'location'


class Patient(models.Model):
    patient = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)
    medical_history = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient'


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    caregiver = models.ForeignKey(Caregiver, models.DO_NOTHING, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(unique=True, max_length=255, blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    payment_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment'


class ShiftReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, models.DO_NOTHING, blank=True, null=True)
    caregiver = models.ForeignKey(Caregiver, models.DO_NOTHING, blank=True, null=True)
    payment = models.ForeignKey(Payment, models.DO_NOTHING, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    report_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shift_report'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    location = models.ForeignKey(Location, models.DO_NOTHING, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=225)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.TextField()  # This field type is a guess.
    address_line = models.CharField(max_length=225, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
