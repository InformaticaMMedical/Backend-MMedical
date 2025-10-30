from rest_framework import serializers
from productos.models.ProductoModel import Producto
from productos.serializers.CategoriaSerializer import CategoriaSerializer
from productos.serializers.ProveedorSerializer import ProveedorSerializer
from productos.serializers.ImagenProductoSerializer import ImagenProductoSerializer
from productos.serializers.ValorAtributoSerializer import ValorAtributoProductoSerializer
from productos.serializers.FabricanteSerializer import ModeloFabricanteSerializer


class ProductoSerializer(serializers.ModelSerializer):
    categoria_detalle = CategoriaSerializer(source="categoria", read_only=True)
    proveedores_detalle = ProveedorSerializer(source="proveedores", many=True, read_only=True)
    modelo_fabricante_detalle = ModeloFabricanteSerializer(source="modelo_fabricante", read_only=True)
    imagenes = ImagenProductoSerializer(many=True, read_only=True)
    valores_atributo = ValorAtributoProductoSerializer(many=True, read_only=True)

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
            "modelo_fabricante_detalle",
            "imagenes",
            "valores_atributo",
        ]
