from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from usuarios.authentication import CookieJWTAuthentication
from productos.serializers.ProductoSerializer import ProductoSerializer
from productos.models.ProductoModel import Producto
from utils.LogUtil import LogUtil


class ProductoListCreateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        productos = Producto.objects.all().prefetch_related("atributos", "marcas", "categoria")
        serializer = ProductoSerializer(productos, many=True)

        LogUtil.registrar_log(
            usuario=request.user,
            accion="CONSULTAR",
            entidad="Producto",
            detalle="Se consulta la lista de productos"
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            producto = serializer.save()

            LogUtil.registrar_log(
                usuario=request.user,
                accion="CREAR",
                entidad="Producto",
                detalle=f"Se crea el producto '{producto.nombre}' (ID {producto.id})"
            )

            return Response(ProductoSerializer(producto).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductoDetailAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return None

    def get(self, request, pk):
        producto = self.get_object(pk)
        if not producto:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductoSerializer(producto)

        LogUtil.registrar_log(
            usuario=request.user,
            accion="CONSULTAR",
            entidad="Producto",
            detalle=f"Se consulta el producto '{producto.nombre}' (ID {producto.id})"
        )

        return Response(serializer.data)

    def put(self, request, pk):
        producto = self.get_object(pk)
        if not producto:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            producto_actualizado = serializer.save()

            LogUtil.registrar_log(
                usuario=request.user,
                accion="EDITAR",
                entidad="Producto",
                detalle=f"Se actualiza el producto '{producto_actualizado.nombre}' (ID {producto_actualizado.id})"
            )

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        producto = self.get_object(pk)
        if not producto:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        nombre = producto.nombre
        producto_id = producto.id
        producto.delete()

        LogUtil.registrar_log(
            usuario=request.user,
            accion="ELIMINAR",
            entidad="Producto",
            detalle=f"Se elimina el producto '{nombre}' (ID {producto_id})"
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
