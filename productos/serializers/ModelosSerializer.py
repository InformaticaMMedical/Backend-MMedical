from rest_framework import serializers
from productos.models.ModelosModel import Modelo

class ModelosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = '__all__'