from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

from ventas.models.models import Cotizacion, CotizacionItem
from ventas.serializers.serializers import (
    CotizacionSerializer,
    CotizacionItemSerializer
)
from productos.models import Producto


class CrearCotizacionAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        cotizacion = Cotizacion.objects.create(
            cliente_nombre=request.data.get("cliente_nombre", ""),
            cliente_email=request.data.get("cliente_email", ""),
            cliente_empresa=request.data.get("cliente_empresa", ""),
            cliente_rut=request.data.get("cliente_rut", ""),
            region=request.data.get("region", ""),
            comuna=request.data.get("comuna", ""),
            direccion=request.data.get("direccion", ""),
            telefono=request.data.get("telefono", ""),
            plazo_entrega=request.data.get("plazo_entrega", ""),
            comentarios=request.data.get("comentarios", ""),
            enviada=True
        )

        return Response(
            {"id": cotizacion.id},
            status=status.HTTP_201_CREATED
        )


class AgregarItemAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

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

        if not producto_id:
            return Response(
                {"error": "producto_id es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )

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
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, cotizacion_id):
        try:
            cotizacion = (
                Cotizacion.objects
                .prefetch_related("items")
                .get(id=cotizacion_id)
            )
        except Cotizacion.DoesNotExist:
            return Response(
                {"error": "No existe"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            CotizacionSerializer(cotizacion).data,
            status=status.HTTP_200_OK
        )

class ActualizarItemCotizacionAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def patch(self, request, item_id):
        try:
            item = CotizacionItem.objects.get(id=item_id)
        except CotizacionItem.DoesNotExist:
            return Response(
                {"error": "Item no existe"},
                status=status.HTTP_404_NOT_FOUND
            )

        cantidad = request.data.get("cantidad")

        if not cantidad or int(cantidad) < 1:
            return Response(
                {"error": "Cantidad inválida"},
                status=status.HTTP_400_BAD_REQUEST
            )

        item.cantidad = int(cantidad)
        item.save()

        return Response(
            CotizacionItemSerializer(item).data,
            status=status.HTTP_200_OK
        )

class EliminarItemCotizacionAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def delete(self, request, item_id):
        try:
            item = CotizacionItem.objects.get(id=item_id)
        except CotizacionItem.DoesNotExist:
            return Response(
                {"error": "Item no existe"},
                status=status.HTTP_404_NOT_FOUND
            )

        item.delete()

        return Response(
            {"message": "Item eliminado correctamente"},
            status=status.HTTP_204_NO_CONTENT
        )
