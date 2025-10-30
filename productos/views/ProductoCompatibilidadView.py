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
        compatibilidades = ProductoCompatibilidad.objects.select_related("producto_principal", "producto_relacionado").all()
        serializer = ProductoCompatibilidadSerializer(compatibilidades, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductoCompatibilidadSerializer(data=request.data)
        if serializer.is_valid():
            compat = serializer.save()
            LogUtil.registrar_log(
                usuario=request.user,
                accion="CREAR",
                entidad="ProductoCompatibilidad",
                detalle=f"Se crea compatibilidad: {compat.producto_principal.nombre} ↔ {compat.producto_relacionado.nombre}"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductoCompatibilidadDetailAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ProductoCompatibilidad.objects.get(pk=pk)
        except ProductoCompatibilidad.DoesNotExist:
            return None

    def get(self, request, pk):
        compat = self.get_object(pk)
        if not compat:
            return Response({"error": "Compatibilidad no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductoCompatibilidadSerializer(compat)
        return Response(serializer.data)

    def put(self, request, pk):
        compat = self.get_object(pk)
        if not compat:
            return Response({"error": "Compatibilidad no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductoCompatibilidadSerializer(compat, data=request.data)
        if serializer.is_valid():
            actualizado = serializer.save()
            LogUtil.registrar_log(
                usuario=request.user,
                accion="EDITAR",
                entidad="ProductoCompatibilidad",
                detalle=f"Se actualiza compatibilidad: {actualizado.producto_principal.nombre} ↔ {actualizado.producto_relacionado.nombre}"
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        compat = self.get_object(pk)
        if not compat:
            return Response({"error": "Compatibilidad no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        nombre_a = compat.producto_principal.nombre
        nombre_b = compat.producto_relacionado.nombre
        compat.delete()
        LogUtil.registrar_log(
            usuario=request.user,
            accion="ELIMINAR",
            entidad="ProductoCompatibilidad",
            detalle=f"Se elimina compatibilidad entre '{nombre_a}' y '{nombre_b}'"
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
