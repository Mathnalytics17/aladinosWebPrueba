from django.db import models
from apps.areaPrivada.api.models.users.index import Socio
from apps.areaPrivada.api.models.users.index import User
# models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
# Define el modelo para almacenar la información de las llamadas realizadas por los fundraisers

class RegistroLlamada(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE)
    fundraiser = models.ForeignKey(User, on_delete=models.CASCADE)  # o tu modelo personalizado
    numero_de_llamada = models.IntegerField(default=1)
    resultado = models.CharField(max_length=100)
    notas = models.TextField(null=True, blank=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Llamada #{self.numero_de_llamada} - {self.socio.nombre} por {self.fundraiser.username}"
    




class UserTrazability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trazability_logs')
    view_name = models.CharField(max_length=255)
    url_path = models.CharField(max_length=500)
    entry_time = models.DateTimeField(default=timezone.now)
    exit_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    # Información del dispositivo
    device_type = models.CharField(max_length=50, null=True, blank=True)  # mobile, tablet, desktop
    browser_name = models.CharField(max_length=100, null=True, blank=True)
    browser_version = models.CharField(max_length=50, null=True, blank=True)
    os_name = models.CharField(max_length=100, null=True, blank=True)
    os_version = models.CharField(max_length=50, null=True, blank=True)
    is_bot = models.BooleanField(default=False)
    device_model = models.CharField(max_length=100, null=True, blank=True)
    
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-entry_time']
        verbose_name_plural = 'User Trazability Logs'
    
    def save(self, *args, **kwargs):
        if self.exit_time and self.entry_time:
            self.duration = self.exit_time - self.entry_time
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.email} - {self.view_name} - {self.device_type}"