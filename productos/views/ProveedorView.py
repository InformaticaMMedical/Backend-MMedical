from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from productos.models.ProveedorModel import Proveedor
from productos.serializers.ProveedorSerializer import ProveedorSerializer
from utils.LogUtil import LogUtil

class ProveedorListCreateAPIView(APIView):
    def get(self, request):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        proveedores = Proveedor.objects.all()
        serializer = ProveedorSerializer(proveedores, many=True)
        return Response(serializer.data)

    def post(self, request):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        serializer = ProveedorSerializer(data=request.data)
        if serializer.is_valid():
            proveedor = serializer.save()
            LogUtil.registrar_log(
                modelo="Proveedor",
                operacion="CREAR",
                descripcion=f"{usuario} creó el proveedor '{proveedor.nombre}'"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProveedorDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Proveedor.objects.get(pk=pk)
        except Proveedor.DoesNotExist:
            return None

    def get(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        proveedor = self.get_object(pk)
        if not proveedor:
            return Response({"error": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProveedorSerializer(proveedor)
        return Response(serializer.data)

    def put(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        proveedor = self.get_object(pk)
        if not proveedor:
            return Response({"error": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProveedorSerializer(proveedor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            LogUtil.registrar_log(
                modelo="Proveedor",
                operacion="ACTUALIZAR",
                descripcion=f"{usuario} actualizó el proveedor '{proveedor.nombre}'"
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        proveedor = self.get_object(pk)
        if not proveedor:
            return Response({"error": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        nombre_proveedor = proveedor.nombre
        proveedor.delete()
        LogUtil.registrar_log(
            modelo="Proveedor",
            operacion="ELIMINAR",
            descripcion=f"{usuario} eliminó el proveedor '{nombre_proveedor}'"
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
