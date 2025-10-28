from rest_framework import serializers
from productos.models.ProveedorModel import Proveedor

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'
