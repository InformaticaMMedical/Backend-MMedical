from rest_framework import serializers
from productos.models.FabricanteModel import Fabricante, ModeloFabricante


class FabricanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabricante
        fields = ["id", "nombre"]


class ModeloFabricanteSerializer(serializers.ModelSerializer):
    fabricante_nombre = serializers.CharField(source="fabricante.nombre", read_only=True)
    fabricante_detalle = FabricanteSerializer(source="fabricante", read_only=True)

    class Meta:
        model = ModeloFabricante
        fields = [
            "id",
            "nombre",
            "fabricante",
            "fabricante_nombre",
            "fabricante_detalle",
        ]
