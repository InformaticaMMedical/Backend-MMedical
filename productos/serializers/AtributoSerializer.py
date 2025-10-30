from rest_framework import serializers
from productos.models.AtributoModel import Atributo

class AtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atributo
        fields = '__all__'
