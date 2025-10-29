from rest_framework import serializers
from productos.models.ImagenProductoModel import ImagenProducto

class ImagenProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenProducto
        fields = ["id", "filename", "url", "created_at"]
        read_only_fields = ["id", "url", "created_at"]
