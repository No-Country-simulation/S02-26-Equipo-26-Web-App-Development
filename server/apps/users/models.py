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