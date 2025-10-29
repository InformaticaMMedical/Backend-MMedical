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
        if categoria_id:
            atributos = Atributo.objects.filter(categorias__id=categoria_id)
        else:
            atributos = Atributo.objects.all()

        serializer = AtributoSerializer(atributos, many=True)

        LogUtil.registrar_log(
            usuario=request.user,
            accion="CONSULTAR",
            entidad="Atributo",
            detalle="Se consulta la lista de atributos"
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = AtributoSerializer(data=request.data)
        if serializer.is_valid():
            atributo = serializer.save()

            LogUtil.registrar_log(
                usuario=request.user,
                accion="CREAR",
                entidad="Atributo",
                detalle=f"Se crea el atributo '{atributo.nombre}'"
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
        atributo = self.get_object(pk)
        if not atributo:
            return Response({"error": "Atributo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AtributoSerializer(atributo)

        LogUtil.registrar_log(
            usuario=request.user,
            accion="CONSULTAR",
            entidad="Atributo",
            detalle=f"Se consulta el atributo '{atributo.nombre}'"
        )

        return Response(serializer.data)

    def put(self, request, pk):
        atributo = self.get_object(pk)
        if not atributo:
            return Response({"error": "Atributo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AtributoSerializer(atributo, data=request.data)
        if serializer.is_valid():
            atributo_actualizado = serializer.save()

            LogUtil.registrar_log(
                usuario=request.user,
                accion="EDITAR",
                entidad="Atributo",
                detalle=f"Se actualiza el atributo '{atributo_actualizado.nombre}'"
            )

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        atributo = self.get_object(pk)
        if not atributo:
            return Response({"error": "Atributo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        nombre_atributo = atributo.nombre
        atributo.delete()

        LogUtil.registrar_log(
            usuario=request.user,
            accion="ELIMINAR",
            entidad="Atributo",
            detalle=f"Se elimina el atributo '{nombre_atributo}'"
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
