from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from productos.models.AtributoModel import Atributo
from productos.serializers.AtributoSerializer import AtributoSerializer
from utils.LogUtil import LogUtil

class AtributoListCreateAPIView(APIView):
    def get(self, request):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        categoria_id = request.query_params.get("categoria")
        if categoria_id:
            atributos = Atributo.objects.filter(categorias__id=categoria_id)
        else:
            atributos = Atributo.objects.all()
        serializer = AtributoSerializer(atributos, many=True)
        LogUtil.registrar_log(
            accion="CONSULTAR",
            entidad="Atributo",
            detalle=f"{usuario} consultó la lista de atributos"
        )
        return Response(serializer.data)

    def post(self, request):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        serializer = AtributoSerializer(data=request.data)
        if serializer.is_valid():
            atributo = serializer.save()
            LogUtil.registrar_log(
                accion="AGREGAR",
                entidad="Atributo",
                detalle=f"{usuario} creó el atributo: {atributo.nombre}"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AtributoDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Atributo.objects.get(pk=pk)
        except Atributo.DoesNotExist:
            return None

    def get(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        atributo = self.get_object(pk)
        if not atributo:
            return Response({"error": "Atributo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AtributoSerializer(atributo)
        LogUtil.registrar_log(
            accion="CONSULTAR",
            entidad="Atributo",
            detalle=f"{usuario} consultó el atributo: {atributo.nombre}"
        )
        return Response(serializer.data)

    def put(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        atributo = self.get_object(pk)
        if not atributo:
            return Response({"error": "Atributo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AtributoSerializer(atributo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            LogUtil.registrar_log(
                accion="EDITAR",
                entidad="Atributo",
                detalle=f"{usuario} actualizó el atributo: {atributo.nombre}"
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        atributo = self.get_object(pk)
        if not atributo:
            return Response({"error": "Atributo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        nombre_atributo = atributo.nombre
        atributo.delete()
        LogUtil.registrar_log(
            accion="ELIMINAR",
            entidad="Atributo",
            detalle=f"{usuario} eliminó el atributo: {nombre_atributo}"
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
