from rest_framework import serializers
from productos.models.ProductoCompatibilidadModel import ProductoCompatibilidad

class ProductoCompatibilidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoCompatibilidad
        fields = '__all__'