from rest_framework import serializers
from productos.models.ProductoCompatibilidadModel import ProductoCompatibilidad
from productos.models.ProductoModel import Producto

class ProductoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ["id", "nombre"]

class ProductoCompatibilidadSerializer(serializers.ModelSerializer):
    producto_principal_detalle = ProductoSimpleSerializer(source="producto_principal", read_only=True)
    producto_relacionado_detalle = ProductoSimpleSerializer(source="producto_relacionado", read_only=True)

    class Meta:
        model = ProductoCompatibilidad
        fields = [
            "id",
            "producto_principal",
            "producto_principal_detalle",
            "producto_relacionado",
            "producto_relacionado_detalle",
            "filename",
            "key",
        ]
