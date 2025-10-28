from rest_framework import serializers
from ..models import Atributo

class AtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atributo
        fields = '__all__'
