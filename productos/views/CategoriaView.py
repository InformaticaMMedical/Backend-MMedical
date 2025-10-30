from productos.models.CategoriaModel import Categoria
from productos.serializers.CategoriaSerializer import CategoriaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from usuarios.authentication import CookieJWTAuthentication
from utils.LogUtil import LogUtil


class CategoriaListCreateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            categoria = serializer.save()
            LogUtil.registrar_log(
                usuario=request.user,
                accion="CREAR",
                entidad="Categoria",
                detalle=f"Se crea la categoría '{categoria.nombre}'"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoriaDetailAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Categoria.objects.get(pk=pk)
        except Categoria.DoesNotExist:
            return None

    def get(self, request, pk):
        categoria = self.get_object(pk)
        if not categoria:
            return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)

    def put(self, request, pk):
        categoria = self.get_object(pk)
        if not categoria:
            return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            categoria_actualizada = serializer.save()
            LogUtil.registrar_log(
                usuario=request.user,
                accion="EDITAR",
                entidad="Categoria",
                detalle=f"Se actualiza la categoría '{categoria_actualizada.nombre}'"
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        categoria = self.get_object(pk)
        if not categoria:
            return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        nombre_categoria = categoria.nombre
        categoria.delete()
        LogUtil.registrar_log(
            usuario=request.user,
            accion="ELIMINAR",
            entidad="Categoria",
            detalle=f"Se elimina la categoría '{nombre_categoria}'"
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
