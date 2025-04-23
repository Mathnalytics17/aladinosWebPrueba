# serializers.py
from rest_framework import serializers
from apps.areaPrivada.api.models.areaAministrador.index import RegistroLlamada

class LlamadaSerializer(serializers.ModelSerializer):
    class Meta:
        model =RegistroLlamada
        fields = '__all__'