from rest_framework import serializers
from ..models import Atributo, ValorAtributoProducto

class AtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atributo
        fields = '__all__'


class ValorAtributoProductoSerializer(serializers.ModelSerializer):
    atributo = AtributoSerializer(read_only=True)

    class Meta:
        model = ValorAtributoProducto
        fields = '__all__'