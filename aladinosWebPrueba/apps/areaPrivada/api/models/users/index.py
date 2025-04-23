# models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
import uuid
    
from django.db import models
from django.contrib.auth import get_user_model
class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "GESTOR", "Gestor"
        JEFE = "JEFE", "Jefe"
        COMERCIAL = "COMERCIAL", "Comercial"
        USER = "USER", "Usuario"

    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    # User status fields
    is_active = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    
    # Role field
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.USER)
    
    # Additional fields
    phone = models.CharField(max_length=20, blank=True)
    fundRaiserCode= models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        from django.utils import timezone
        return timezone.now() < self.expires_at

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        from django.utils import timezone
        return timezone.now() < self.expires_at


User = get_user_model()

class Socio(models.Model):
    # Información personal
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    nombre_socio = models.CharField(max_length=100)
    apellido_socio = models.CharField(max_length=100)
    genero_socio = models.CharField(max_length=10)
    
    # Identificación
    tipo_identificacion_socio = models.CharField(max_length=20)
    numero_identificacion_socio = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    
    # Dirección
    via_principal = models.CharField(max_length=255)
    cp_direccion = models.CharField(max_length=10)
    ciudad_direccion = models.CharField(max_length=100)
    estado_provincia = models.CharField(max_length=100)
    
    # Información de pago
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    periodicidad = models.CharField(max_length=20)
    dia_presentacion = models.CharField(default="1", max_length=255)
    medio_pago = models.CharField(max_length=20)
    tipo_pago = models.CharField(max_length=20)
    
    # Relación con fundraiser (usuario COMERCIAL)
    fundraiser = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'COMERCIAL'},
        related_name='socios_captados'
    )
    
    # Información de captación
    primer_canal_captacion = models.CharField(max_length=100)
    canal_entrada = models.CharField(max_length=50)
    
    # Metadata
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    status=models.CharField(default='Pendiente',max_length=255)
    devolucion=models.BooleanField(default=False)
    telefono=models.CharField(max_length=20, blank=True)
    no_llamadas=models.IntegerField(default=0)
    fecha_verificacion=models.DateTimeField(null=True, blank=True)
    class Meta:
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'
        ordering = ['-fecha_alta']
        indexes = [
            models.Index(fields=['numero_identificacion_socio']),
            models.Index(fields=['fundraiser']),
            models.Index(fields=['fecha_alta']),
        ]

    def __str__(self):
        return f"{self.nombre_socio} {self.apellido_socio} ({self.numero_identificacion_socio})"
