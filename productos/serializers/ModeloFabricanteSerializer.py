from rest_framework import serializers
from productos.models.ModeloFabricanteModel import ModeloFabricante

class ModeloFabricanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeloFabricante
        fields = '__all__'
