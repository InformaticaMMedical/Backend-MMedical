from rest_framework import serializers
from productos.models.ProductoModel import Producto
from productos.serializers.CategoriaSerializer import CategoriaSerializer
from productos.serializers.ProveedorSerializer import ProveedorSerializer
from productos.serializers.ImagenProductoSerializer import ImagenProductoSerializer
from productos.serializers.ValorAtributoSerializer import ValorAtributoProductoSerializer
from productos.models.ArchivoProducto import ArchivoProducto


class ArchivoProductoSerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField()

    class Meta:
        model = ArchivoProducto
        fields = ["id", "producto", "filename", "key"]

    def get_key(self, obj):
        request = self.context.get("request")

        if not obj.key:
            return ""

        if obj.key.startswith("http://") or obj.key.startswith("https://"):
            return obj.key

        if obj.key.startswith("/"):
            if request:
                return request.build_absolute_uri(obj.key)
            return obj.key

        if request:
            return request.build_absolute_uri(f"/media/{obj.key}")

        return f"/media/{obj.key}"



class ProductoSerializer(serializers.ModelSerializer):
    categoria_detalle = CategoriaSerializer(source="categoria", read_only=True)
    proveedores_detalle = ProveedorSerializer(source="proveedores", many=True, read_only=True)

    imagenes = ImagenProductoSerializer(many=True, read_only=True)

    valores_atributo = ValorAtributoProductoSerializer(
        source="atributos",
        many=True,
        read_only=True
    )

    archivos = ArchivoProductoSerializer(many=True, read_only=True)

    class Meta:
        model = Producto
        fields = [
            "id",
            "nombre",
            "descripcion",
            "categoria",
            "categoria_detalle",
            "proveedores",
            "proveedores_detalle",
            "modelo_fabricante",
            "imagenes",
            "archivos",
            "valores_atributo",
        ]
