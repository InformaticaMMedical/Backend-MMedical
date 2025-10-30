from rest_framework import serializers
from productos.models.ImagenProductoModel import ImagenProducto

class ImagenProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenProducto
        fields = ["id", "producto", "filename", "key"]
        read_only_fields = ["id"]
