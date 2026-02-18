from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator


class UserRole(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    CAREGIVER = 'Caregiver', 'Caregiver'
    PATIENT = 'Patient', 'Patient'


class Location(models.Model):
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    class Meta:
        db_table = 'location'
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return f"{self.city}, {self.country}"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', UserRole.ADMIN)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número debe estar en formato: '+999999999'. Hasta 15 dígitos permitidos."
    )
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=UserRole.choices)
    address_line = models.CharField(max_length=225, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


# ========== PATIENT MODEL ==========
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='patient_profile')
    medical_history = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'patient'
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def __str__(self):
        return f"Patient: {self.user.full_name}"


# ========== CAREGIVER MODEL ==========
class Caregiver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='caregiver_profile')
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bank_account = models.CharField(max_length=25, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'caregiver'
        verbose_name = 'Caregiver'
        verbose_name_plural = 'Caregivers'

    def __str__(self):
        return f"Caregiver: {self.user.full_name}"


# ========== ADMIN MODEL ==========
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='admin_profile')
    access_level = models.IntegerField(default=1)

    class Meta:
        db_table = 'admin'
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

    def __str__(self):
        return f"Admin: {self.user.full_name}"


# ========== FAMILY MODEL ==========
class Family(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='family_members')
    relationship = models.CharField(max_length=50)

    class Meta:
        db_table = 'family'
        verbose_name = 'Family Member'
        verbose_name_plural = 'Family Members'

    def __str__(self):
        return f"{self.relationship} of {self.patient.user.full_name}"


# ========== DOCUMENT MODEL ==========
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
    verification_status = models.CharField(max_length=20, choices=DocumentStatus.choices, default=DocumentStatus.PENDING)
    rejection_reason = models.TextField(blank=True, null=True)
    verified_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_documents')

    class Meta:
        db_table = 'document'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return f"{self.document_type} - {self.caregiver.user.full_name}"


# ========== PAYMENT MODEL ==========
class PaymentStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    SUCCESS = 'Success', 'Success'
    FAILED = 'Failed', 'Failed'


class Payment(models.Model):
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'payment'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f"Payment {self.id} - {self.caregiver.user.full_name}"


# ========== SHIFT REPORT MODEL ==========
class ShiftReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='shift_reports')
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE, related_name='shift_reports')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='shift_reports')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    report_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'shift_report'
        verbose_name = 'Shift Report'
        verbose_name_plural = 'Shift Reports'

    def __str__(self):
        return f"Shift {self.id} - {self.caregiver.user.full_name}"

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            self.total_hours = round(duration.total_seconds() / 3600, 2)
        super().save(*args, **kwargs)