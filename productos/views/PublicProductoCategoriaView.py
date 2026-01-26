from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from productos.models.ProductoModel import Producto
from productos.serializers.ProductoSerializer import ProductoSerializer


class PublicProductoPorCategoriaAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, categoria_nombre):
        productos = (
            Producto.objects
            .filter(categoria__nombre__iexact=categoria_nombre)
            .select_related("categoria", "modelo_fabricante")
            .prefetch_related("proveedores", "atributos", "archivos")
        )

        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
