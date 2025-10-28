from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from productos.serializers.ProductoSerializer import ProductoSerializer
from productos.models.ProductoModel import Producto
from utils.LogUtil import LogUtil

class ProductoListCreateAPIView(APIView):
    def get(self, request):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        productos = Producto.objects.all().prefetch_related("atributos", "marcas", "categoria")
        serializer = ProductoSerializer(productos, many=True)
        LogUtil.registrar_log(
            accion="CONSULTAR",
            entidad="Producto",
            detalle=f"{usuario} consultó la lista de productos"
        )
        return Response(serializer.data)

    def post(self, request):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            producto = serializer.save()
            LogUtil.registrar_log(
                accion="AGREGAR",
                entidad="Producto",
                detalle=f"{usuario} agregó el producto '{producto.nombre}' con ID {producto.id}"
            )
            return Response(ProductoSerializer(producto).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductoDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return None

    def get(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        producto = self.get_object(pk)
        if not producto:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductoSerializer(producto)
        LogUtil.registrar_log(
            accion="CONSULTAR",
            entidad="Producto",
            detalle=f"{usuario} consultó el producto '{producto.nombre}' (ID {producto.id})"
        )
        return Response(serializer.data)

    def put(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        producto = self.get_object(pk)
        if not producto:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            producto = serializer.save()
            LogUtil.registrar_log(
                accion="EDITAR",
                entidad="Producto",
                detalle=f"{usuario} editó el producto '{producto.nombre}' (ID {producto.id})"
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        producto = self.get_object(pk)
        if not producto:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        nombre = producto.nombre
        producto_id = producto.id
        producto.delete()
        LogUtil.registrar_log(
            accion="ELIMINAR",
            entidad="Producto",
            detalle=f"{usuario} eliminó el producto '{nombre}' (ID {producto_id})"
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
