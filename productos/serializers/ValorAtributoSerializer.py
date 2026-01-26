from rest_framework import serializers
from productos.models.ValorAtributoProductoModel import ValorAtributoProducto


class ValorAtributoProductoSerializer(serializers.ModelSerializer):
    atributo_nombre = serializers.CharField(source="atributo.nombre", read_only=True)

    class Meta:
        model = ValorAtributoProducto
        fields = [
            "id",
            "producto",
            "atributo",
            "atributo_nombre",
            "valor_texto",
            "valor_numero",
            "valor_booleano",
            "valor_fecha",
        ]
