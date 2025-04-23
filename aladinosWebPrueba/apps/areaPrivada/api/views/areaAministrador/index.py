# views.py
from rest_framework import viewsets
from apps.areaPrivada.api.serializers.areaAministrador.index import LlamadaSerializer
from apps.areaPrivada.api.models.areaAministrador.index import RegistroLlamada

class LlamadaViewSet(viewsets.ModelViewSet):
    queryset = RegistroLlamada.objects.all()
    serializer_class = LlamadaSerializer
