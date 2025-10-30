from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from usuarios.authentication import CookieJWTAuthentication
from productos.models.AtributoModel import Atributo
from productos.serializers.AtributoSerializer import AtributoSerializer
from utils.LogUtil import LogUtil


class AtributoListCreateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categoria_id = request.query_params.get("categoria")
        qs = Atributo.objects.all()
        if categoria_id:
            qs = qs.filter(categorias__id=categoria_id)
        serializer = AtributoSerializer(qs, many=True)
        LogUtil.registrar_log(
            usuario=request.user, accion="CONSULTAR",
            entidad="Atributo", detalle="Se consulta la lista de atributos"
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = AtributoSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            LogUtil.registrar_log(
                usuario=request.user, accion="CREAR",
                entidad="Atributo", detalle=f"Se crea el atributo '{obj.nombre}'"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AtributoDetailAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Atributo.objects.get(pk=pk)
        except Atributo.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Atributo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AtributoSerializer(obj)
        LogUtil.registrar_log(
            usuario=request.user, accion="CONSULTAR",
            entidad="Atributo", detalle=f"Se consulta el atributo '{obj.nombre}'"
        )
        return Response(serializer.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Atributo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AtributoSerializer(obj, data=request.data)
        if serializer.is_valid():
            actualizado = serializer.save()
            LogUtil.registrar_log(
                usuario=request.user, accion="EDITAR",
                entidad="Atributo", detalle=f"Se actualiza el atributo '{actualizado.nombre}'"
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Atributo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        nombre = obj.nombre
        obj.delete()
        LogUtil.registrar_log(
            usuario=request.user, accion="ELIMINAR",
            entidad="Atributo", detalle=f"Se elimina el atributo '{nombre}'"
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
