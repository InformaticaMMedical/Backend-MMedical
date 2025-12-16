from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ventas.models.models import Cotizacion, CotizacionItem
from ventas.serializers.serializers import ( CotizacionSerializer, CotizacionItemSerializer)
from productos.models import Producto


class CrearCotizacionAPIView(APIView):
    def post(self, request):
        cotizacion = Cotizacion.objects.create(
            cliente_nombre=request.data.get("cliente_nombre", ""),
            cliente_email=request.data.get("cliente_email", ""),
            cliente_empresa=request.data.get("cliente_empresa", "")
        )

        # 👇 CLAVE: devolver "id"
        return Response(
            {
                "id": cotizacion.id
            },
            status=status.HTTP_201_CREATED
        )


class AgregarItemAPIView(APIView):
    def post(self, request, cotizacion_id):
        try:
            cotizacion = Cotizacion.objects.get(id=cotizacion_id)
        except Cotizacion.DoesNotExist:
            return Response(
                {"error": "Cotización no existe"},
                status=status.HTTP_404_NOT_FOUND
            )

        producto_id = request.data.get("producto_id")
        cantidad = request.data.get("cantidad", 1)

        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return Response(
                {"error": "Producto no existe"},
                status=status.HTTP_404_NOT_FOUND
            )

        item = CotizacionItem.objects.create(
            cotizacion=cotizacion,
            producto=producto,
            cantidad=cantidad
        )

        return Response(
            CotizacionItemSerializer(item).data,
            status=status.HTTP_201_CREATED
        )


class ObtenerCotizacionAPIView(APIView):
    def get(self, request, cotizacion_id):
        try:
            cotizacion = Cotizacion.objects.get(id=cotizacion_id)
        except Cotizacion.DoesNotExist:
            return Response(
                {"error": "No existe"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(CotizacionSerializer(cotizacion).data)
