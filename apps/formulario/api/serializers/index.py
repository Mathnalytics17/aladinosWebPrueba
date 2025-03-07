# Serializador
from rest_framework import serializers

from apps.formulario.api.models.index import Formulario

class FormularioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formulario
        fields = '__all__'