from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from productos.models.ProductoCompatibilidadModel import ProductoCompatibilidad
from productos.serializers.ProductoCompatibilidadSerializer import ProductoCompatibilidadSerializer
from utils.LogUtil import LogUtil

class ProductoCompatibilidadListCreateAPIView(APIView):
    def get(self, request):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        compatibilidades = ProductoCompatibilidad.objects.select_related("producto", "modelo").all()
        serializer = ProductoCompatibilidadSerializer(compatibilidades, many=True)
        LogUtil.registrar_log(
            accion="CONSULTAR",
            entidad="ProductoCompatibilidad",
            detalle=f"{usuario} consultó la lista de compatibilidades de productos"
        )
        return Response(serializer.data)

    def post(self, request):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        serializer = ProductoCompatibilidadSerializer(data=request.data)
        if serializer.is_valid():
            compatibilidad = serializer.save()
            LogUtil.registrar_log(
                accion="CREAR",
                entidad="ProductoCompatibilidad",
                detalle=f"{usuario} agregó compatibilidad del producto '{compatibilidad.producto.nombre}' con modelo '{compatibilidad.modelo.nombre}'"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductoCompatibilidadDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return ProductoCompatibilidad.objects.select_related("producto", "modelo").get(pk=pk)
        except ProductoCompatibilidad.DoesNotExist:
            return None

    def get(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        compatibilidad = self.get_object(pk)
        if not compatibilidad:
            return Response({"error": "Compatibilidad no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductoCompatibilidadSerializer(compatibilidad)
        LogUtil.registrar_log(
            accion="CONSULTAR",
            entidad="ProductoCompatibilidad",
            detalle=f"{usuario} consultó compatibilidad del producto '{compatibilidad.producto.nombre}' con modelo '{compatibilidad.modelo.nombre}'"
        )
        return Response(serializer.data)

    def put(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        compatibilidad = self.get_object(pk)
        if not compatibilidad:
            return Response({"error": "Compatibilidad no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductoCompatibilidadSerializer(compatibilidad, data=request.data)
        if serializer.is_valid():
            compatibilidad = serializer.save()
            LogUtil.registrar_log(
                accion="ACTUALIZAR",
                entidad="ProductoCompatibilidad",
                detalle=f"{usuario} actualizó compatibilidad del producto '{compatibilidad.producto.nombre}' con modelo '{compatibilidad.modelo.nombre}'"
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        compatibilidad = self.get_object(pk)
        if not compatibilidad:
            return Response({"error": "Compatibilidad no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        producto_nombre = compatibilidad.producto.nombre
        modelo_nombre = compatibilidad.modelo.nombre
        compatibilidad.delete()
        LogUtil.registrar_log(
            accion="ELIMINAR",
            entidad="ProductoCompatibilidad",
            detalle=f"{usuario} eliminó compatibilidad entre producto '{producto_nombre}' y modelo '{modelo_nombre}'"
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
