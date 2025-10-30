from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from usuarios.authentication import CookieJWTAuthentication
from productos.models.ProveedorModel import Proveedor
from productos.serializers.ProveedorSerializer import ProveedorSerializer
from utils.LogUtil import LogUtil


class ProveedorListCreateAPIView(APIView):
    """
    Listado y creación de proveedores.
    """
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        proveedores = Proveedor.objects.all().order_by("nombre")
        serializer = ProveedorSerializer(proveedores, many=True)

        LogUtil.registrar_log(
            usuario=request.user,
            accion="CONSULTAR",
            entidad="Proveedor",
            detalle="Se consulta la lista de proveedores"
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = ProveedorSerializer(data=request.data)
        if serializer.is_valid():
            proveedor = serializer.save()

            LogUtil.registrar_log(
                usuario=request.user,
                accion="CREAR",
                entidad="Proveedor",
                detalle=f"Se crea el proveedor '{proveedor.nombre}'"
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProveedorDetailAPIView(APIView):
    """
    Consulta, edición y eliminación de un proveedor específico.
    """
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Proveedor.objects.get(pk=pk)
        except Proveedor.DoesNotExist:
            return None

    def get(self, request, pk):
        proveedor = self.get_object(pk)
        if not proveedor:
            return Response({"error": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProveedorSerializer(proveedor)

        LogUtil.registrar_log(
            usuario=request.user,
            accion="CONSULTAR",
            entidad="Proveedor",
            detalle=f"Se consulta el proveedor '{proveedor.nombre}'"
        )

        return Response(serializer.data)

    def put(self, request, pk):
        proveedor = self.get_object(pk)
        if not proveedor:
            return Response({"error": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProveedorSerializer(proveedor, data=request.data)
        if serializer.is_valid():
            actualizado = serializer.save()

            LogUtil.registrar_log(
                usuario=request.user,
                accion="EDITAR",
                entidad="Proveedor",
                detalle=f"Se actualiza el proveedor '{actualizado.nombre}'"
            )

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        proveedor = self.get_object(pk)
        if not proveedor:
            return Response({"error": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        nombre = proveedor.nombre
        proveedor.delete()

        LogUtil.registrar_log(
            usuario=request.user,
            accion="ELIMINAR",
            entidad="Proveedor",
            detalle=f"Se elimina el proveedor '{nombre}'"
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
