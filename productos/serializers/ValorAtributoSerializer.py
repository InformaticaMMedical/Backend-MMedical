from rest_framework import serializers
from productos.models.ValorAtributoModel import ValorAtributoProducto

class ValorAtributoProductoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)

    class Meta:
        model = ValorAtributoProducto
        fields = ["id", "producto", "producto_nombre", "filename", "key"]
