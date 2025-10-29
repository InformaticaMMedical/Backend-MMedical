from rest_framework import serializers
from productos.models.ProductoModel import Producto
from productos.serializers import CategoriaSerializer, ProveedorSerializer
from productos.serializers.ValorAtributoSerializer import ValorAtributoProductoSerializer
from productos.serializers.ImagenProductoSerializer import ImagenProductoSerializer

class ProductoSerializer(serializers.ModelSerializer):
    categoria_detalle = CategoriaSerializer(source='categoria', read_only=True)
    proveedores_detalle = ProveedorSerializer(source='proveedores', many=True, read_only=True)
    atributos = ValorAtributoProductoSerializer(many=True, read_only=True)
    imagenes = ImagenProductoSerializer(many=True, read_only=True)  # <--- Aquí

    categoria = serializers.PrimaryKeyRelatedField(
        queryset=Producto._meta.get_field('categoria').remote_field.model.objects.all(),
        required=True
    )
    proveedores = serializers.PrimaryKeyRelatedField(
        queryset=Producto._meta.get_field('proveedores').remote_field.model.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'categoria',
            'categoria_detalle',
            'proveedores',
            'proveedores_detalle',
            'atributos',
            'imagenes',
        ]