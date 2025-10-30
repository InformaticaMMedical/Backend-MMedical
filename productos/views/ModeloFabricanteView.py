from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from productos.models.FabricanteModel import ModeloFabricante
from usuarios.authentication import CookieJWTAuthentication
from utils.LogUtil import LogUtil


class ModeloFabricanteListCreateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fabricante_id = request.query_params.get("fabricante")
        modelos = ModeloFabricante.objects.select_related("fabricante").all()

        if fabricante_id:
            modelos = modelos.filter(fabricante_id=fabricante_id)


        LogUtil.registrar_log(
            usuario=request.user,
            accion="CONSULTAR",
            entidad="ModeloFabricante",
            detalle=f"Se consulta la lista de modelos de fabricante (filtro={fabricante_id or 'todos'})"
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = ModeloFabricanteSerializer(data=request.data)
        if serializer.is_valid():
            modelo = serializer.save()

            LogUtil.registrar_log(
                usuario=request.user,
                accion="CREAR",
                entidad="ModeloFabricante",
                detalle=f"Se crea el modelo '{modelo.nombre}' del fabricante '{modelo.fabricante.nombre}'"
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModeloFabricanteDetailAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ModeloFabricante.objects.select_related("fabricante").get(pk=pk)
        except ModeloFabricante.DoesNotExist:
            return None

    def get(self, request, pk):
        modelo = self.get_object(pk)
        if not modelo:
            return Response({"error": "Modelo de fabricante no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ModeloFabricanteSerializer(modelo)

        LogUtil.registrar_log(
            usuario=request.user,
            accion="CONSULTAR",
            entidad="ModeloFabricante",
            detalle=f"Se consulta el modelo '{modelo.nombre}' del fabricante '{modelo.fabricante.nombre}'"
        )

        return Response(serializer.data)

    def put(self, request, pk):
        modelo = self.get_object(pk)
        if not modelo:
            return Response({"error": "Modelo de fabricante no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ModeloFabricanteSerializer(modelo, data=request.data)
        if serializer.is_valid():
            modelo_actualizado = serializer.save()

            LogUtil.registrar_log(
                usuario=request.user,
                accion="EDITAR",
                entidad="ModeloFabricante",
                detalle=f"Se actualiza el modelo '{modelo_actualizado.nombre}' del fabricante '{modelo_actualizado.fabricante.nombre}'"
            )

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        modelo = self.get_object(pk)
        if not modelo:
            return Response({"error": "Modelo de fabricante no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        nombre_modelo = modelo.nombre
        nombre_fabricante = modelo.fabricante.nombre
        modelo.delete()

        LogUtil.registrar_log(
            usuario=request.user,
            accion="ELIMINAR",
            entidad="ModeloFabricante",
            detalle=f"Se elimina el modelo '{nombre_modelo}' del fabricante '{nombre_fabricante}'"
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
