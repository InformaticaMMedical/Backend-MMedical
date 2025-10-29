from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from usuarios.authentication import CookieJWTAuthentication
from productos.models.ProductoCompatibilidadModel import ProductoCompatibilidad
from productos.serializers.ProductoCompatibilidadSerializer import ProductoCompatibilidadSerializer
from utils.LogUtil import LogUtil


class ProductoCompatibilidadListCreateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        compatibilidades = ProductoCompatibilidad.objects.select_related("producto", "modelo").all()
        serializer = ProductoCompatibilidadSerializer(compatibilidades, many=True)

        LogUtil.registrar_log(
            usuario=request.user,
            accion="CONSULTAR",
            entidad="ProductoCompatibilidad",
            detalle="Se consulta la lista de compatibilidades de productos"
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = ProductoCompatibilidadSerializer(data=request.data)
        if serializer.is_valid():
            compatibilidad = serializer.save()

            LogUtil.registrar_log(
                usuario=request.user,
                accion="CREAR",
                entidad="ProductoCompatibilidad",
                detalle=f"Se crea compatibilidad del producto '{compatibilidad.producto.nombre}' con modelo '{compatibilidad.modelo.nombre}'"
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductoCompatibilidadDetailAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ProductoCompatibilidad.objects.select_related("producto", "modelo").get(pk=pk)
        except ProductoCompatibilidad.DoesNotExist:
            return None

    def get(self, request, pk):
        compatibilidad = self.get_object(pk)
        if not compatibilidad:
            return Response({"error": "Compatibilidad no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductoCompatibilidadSerializer(compatibilidad)

        LogUtil.registrar_log(
            usuario=request.user,
            accion="CONSULTAR",
            entidad="ProductoCompatibilidad",
            detalle=f"Se consulta compatibilidad del producto '{compatibilidad.producto.nombre}' con modelo '{compatibilidad.modelo.nombre}'"
        )

        return Response(serializer.data)

    def put(self, request, pk):
        compatibilidad = self.get_object(pk)
        if not compatibilidad:
            return Response({"error": "Compatibilidad no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductoCompatibilidadSerializer(compatibilidad, data=request.data)
        if serializer.is_valid():
            compatibilidad_actualizada = serializer.save()

            LogUtil.registrar_log(
                usuario=request.user,
                accion="EDITAR",
                entidad="ProductoCompatibilidad",
                detalle=f"Se actualiza compatibilidad del producto '{compatibilidad_actualizada.producto.nombre}' con modelo '{compatibilidad_actualizada.modelo.nombre}'"
            )

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        compatibilidad = self.get_object(pk)
        if not compatibilidad:
            return Response({"error": "Compatibilidad no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        producto_nombre = compatibilidad.producto.nombre
        modelo_nombre = compatibilidad.modelo.nombre
        compatibilidad.delete()

        LogUtil.registrar_log(
            usuario=request.user,
            accion="ELIMINAR",
            entidad="ProductoCompatibilidad",
            detalle=f"Se elimina compatibilidad entre producto '{producto_nombre}' y modelo '{modelo_nombre}'"
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
