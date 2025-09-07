# serializers.py
from rest_framework import serializers
from apps.areaPrivada.api.models.areaAministrador.index import RegistroLlamada

from apps.areaPrivada.api.models.areaAministrador.index import UserTrazability
class LlamadaSerializer(serializers.ModelSerializer):
    class Meta:
        model =RegistroLlamada
        fields = '__all__'
        
        
# serializers.py


class UserTrazabilitySerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = UserTrazability
        fields = '__all__'
        read_only_fields = ('created_at', 'duration')