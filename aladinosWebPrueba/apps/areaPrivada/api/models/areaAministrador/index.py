from django.db import models
from apps.areaPrivada.api.models.users.index import Socio
from apps.areaPrivada.api.models.users.index import User
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