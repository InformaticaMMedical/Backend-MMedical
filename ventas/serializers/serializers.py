from rest_framework import serializers
from ventas.models.models import Cotizacion, CotizacionItem


class CotizacionItemSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(
        source="producto.nombre",
        read_only=True
    )

    class Meta:
        model = CotizacionItem
        fields = ['id', 'producto', 'producto_nombre', 'cantidad']


class CotizacionSerializer(serializers.ModelSerializer):
    items = CotizacionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cotizacion
        fields = [
            'id',
            'cliente_nombre',
            'cliente_email',
            'cliente_empresa',
            'cliente_rut',
            'region',
            'comuna',
            'direccion',
            'telefono',
            'plazo_entrega',
            'comentarios',
            'fecha_creacion',
            'enviada',
            'items'
        ]
