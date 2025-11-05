from rest_framework import serializers
from productos.models.ProductoModel import Producto
from productos.models.ProductoCompatibilidadModel import ProductoCompatibilidad 
from productos.models.ValorAtributoModel import ValorAtributoProducto 
from productos.models.FabricanteModel import ModeloFabricante
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

    atributos = serializers.ListField(write_only=True, required=False)
    modelos = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    fabricante = serializers.IntegerField(write_only=True, required=False, allow_null=True)

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
            "fabricante",
            "modelos",
            "atributos",
        ]

    def create(self, validated_data):
        atributos_data = validated_data.pop('atributos', [])
        modelos_data = validated_data.pop('modelos', [])
        fabricante_id = validated_data.pop('fabricante', None)
        proveedores_data = validated_data.pop('proveedores', [])

        # Crear producto sin los M2M
        producto = Producto.objects.create(**validated_data)

        # Asignar fabricante si existe y es válido
        if fabricante_id:
            if ModeloFabricante.objects.filter(id=fabricante_id).exists():
                producto.modelo_fabricante_id = fabricante_id
                producto.save()
            else:
                print(f"⚠️ ModeloFabricante con id={fabricante_id} no existe, se omite asignación.")

        # Asignar proveedores (ManyToMany)
        if proveedores_data:
            producto.proveedores.set(proveedores_data)

        # Crear compatibilidades
        for modelo_id in modelos_data:
            ProductoCompatibilidad.objects.create(producto=producto, modelo_id=modelo_id)

        # Crear valores de atributos (adaptado a tu modelo)
        for attr in atributos_data:
            ValorAtributoProducto.objects.create(
                producto=producto,
                key=attr.get("key", ""),      
                filename=attr.get("filename", "") 
            )

        return producto
