from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from productos.models.ModeloFabricanteModel import ModeloFabricante
from productos.serializers.ModeloFabricanteSerializer import ModeloFabricanteSerializer
from utils.LogUtil import LogUtil

class ModeloFabricanteListCreateAPIView(APIView):
    def get(self, request):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        fabricante_id = request.query_params.get("fabricante")
        modelos = ModeloFabricante.objects.select_related("fabricante").all()

        if fabricante_id:
            modelos = modelos.filter(fabricante_id=fabricante_id)

        serializer = ModeloFabricanteSerializer(modelos, many=True)

        LogUtil.registrar_log(
            accion="CONSULTAR",
            entidad="ModeloFabricante",
            detalle=f"{usuario} consultó la lista de modelos de fabricante (filtro={fabricante_id or 'todos'})"
        )
        return Response(serializer.data)

    def post(self, request):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        serializer = ModeloFabricanteSerializer(data=request.data)
        if serializer.is_valid():
            modelo = serializer.save()
            LogUtil.registrar_log(
                accion="CREAR",
                entidad="ModeloFabricante",
                detalle=f"{usuario} creó el modelo '{modelo.nombre}' del fabricante '{modelo.fabricante.nombre}'"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModeloFabricanteDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return ModeloFabricante.objects.select_related("fabricante").get(pk=pk)
        except ModeloFabricante.DoesNotExist:
            return None

    def get(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        modelo = self.get_object(pk)
        if not modelo:
            return Response({"error": "Modelo de fabricante no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ModeloFabricanteSerializer(modelo)
        LogUtil.registrar_log(
            accion="CONSULTAR",
            entidad="ModeloFabricante",
            detalle=f"{usuario} consultó el modelo '{modelo.nombre}' del fabricante '{modelo.fabricante.nombre}'"
        )
        return Response(serializer.data)

    def put(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        modelo = self.get_object(pk)
        if not modelo:
            return Response({"error": "Modelo de fabricante no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ModeloFabricanteSerializer(modelo, data=request.data)
        if serializer.is_valid():
            modelo = serializer.save()
            LogUtil.registrar_log(
                accion="ACTUALIZAR",
                entidad="ModeloFabricante",
                detalle=f"{usuario} actualizó el modelo '{modelo.nombre}' del fabricante '{modelo.fabricante.nombre}'"
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        modelo = self.get_object(pk)
        if not modelo:
            return Response({"error": "Modelo de fabricante no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        nombre_modelo = modelo.nombre
        nombre_fabricante = modelo.fabricante.nombre
        modelo.delete()
        LogUtil.registrar_log(
            accion="ELIMINAR",
            entidad="ModeloFabricante",
            detalle=f"{usuario} eliminó el modelo '{nombre_modelo}' del fabricante '{nombre_fabricante}'"
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
