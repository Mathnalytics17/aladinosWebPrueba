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

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para crear automáticamente
        un fundraiser cuando se crea un usuario COMERCIAL
        """
        is_new = not self.pk  # Verifica si es un nuevo usuario (no tiene ID aún)
        
        # Guarda primero el usuario
        super().save(*args, **kwargs)
        
        # Solo para nuevos usuarios COMERCIALES con fundRaiserCode
        if is_new and self.role == self.Role.COMERCIAL and self.fundRaiserCode:
            from apps.areaPrivada.api.models.users.index import Fundraiser  # Importación local para evitar circular imports
            Fundraiser.objects.create(
                user=self,
                first_name=self.first_name,
                last_name=self.last_name,
                fundraiser_code=self.fundRaiserCode
            )

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
    nombre_socio = models.CharField(max_length=100, blank=True, null=True)
    apellido_socio = models.CharField(max_length=100, blank=True, null=True)
    genero_socio = models.CharField(max_length=10, blank=True, null=True)
    no_iban = models.CharField(max_length=200, blank=True, null=True)
    
    # Identificación
    tipo_identificacion_socio = models.CharField(max_length=20, blank=True, null=True)
    numero_identificacion_socio = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    telefono_socio = models.CharField(max_length=200, blank=True, null=True)
    email_socio = models.EmailField(max_length=100, blank=True, null=True)
    fecha_alta_real = models.DateField(blank=True, null=True)
    
    # Dirección
    via_principal = models.CharField(max_length=255, blank=True, null=True)
    cp_direccion = models.CharField(max_length=10, blank=True, null=True)
    ciudad_direccion = models.CharField(max_length=100, blank=True, null=True)
    estado_provincia = models.CharField(max_length=100, blank=True, null=True)
    
    # Información de pago
    importe = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    periodicidad = models.CharField(max_length=20, blank=True, null=True)
    dia_presentacion = models.CharField(default="1", max_length=255, blank=True, null=True)
    medio_pago = models.CharField(max_length=20, blank=True, null=True)
    tipo_pago = models.CharField(max_length=20, blank=True, null=True)
    
    # Relación con fundraiser
    fundraiser = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'COMERCIAL'},
        related_name='socios_captados'
    )
    
    # Información de captación
    primer_canal_captacion = models.CharField(max_length=100, blank=True, null=True)
    canal_entrada = models.CharField(max_length=50, blank=True, null=True)
    
    # Metadata
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    status = models.CharField(default='Pendiente', max_length=255, blank=True, null=True)
    devolucion = models.BooleanField(default=False)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    no_llamadas = models.IntegerField(default=0)
    fecha_verificacion = models.DateTimeField(null=True, blank=True)
    is_borrador = models.BooleanField(default=False)

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


class Fundraiser(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='fundraisers',
        verbose_name='Usuario asociado'
    )
    first_name = models.CharField(max_length=100, verbose_name='Nombre')
    last_name = models.CharField(max_length=100, verbose_name='Apellido')
    fundraiser_code = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name='Código de fundraiser'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Fundraiser'
        verbose_name_plural = 'Fundraisers'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.fundraiser_code})"