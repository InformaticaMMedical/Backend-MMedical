from productos.models.CategoriaModel import Categoria
from productos.serializers.CategoriaSerializer import CategoriaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.LogUtil import LogUtil

class CategoriaListCreateAPIView(APIView):
    def get(self, request):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

    def post(self, request):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            categoria = serializer.save()
            LogUtil.registrar_log(
                accion="CREAR",
                entidad="Categoria",
                detalle=f"{usuario} creó la categoría '{categoria.nombre}'"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoriaDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Categoria.objects.get(pk=pk)
        except Categoria.DoesNotExist:
            return None

    def get(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        categoria = self.get_object(pk)
        if not categoria:
            return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)

    def put(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        categoria = self.get_object(pk)
        if not categoria:
            return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            LogUtil.registrar_log(
                accion="EDITAR",
                entidad="Categoria",
                detalle=f"{usuario} actualizó la categoría '{categoria.nombre}'"
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        categoria = self.get_object(pk)
        if not categoria:
            return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        nombre_categoria = categoria.nombre
        categoria.delete()
        LogUtil.registrar_log(
            accion="ELIMINAR",
            entidad="Categoria",
            detalle=f"{usuario} eliminó la categoría '{nombre_categoria}'"
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
