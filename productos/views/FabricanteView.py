from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from productos.models.FabricanteModel import Fabricante
from productos.serializers.FabricanteSerializer import FabricanteSerializer
from utils.LogUtil import LogUtil

class FabricanteListCreateAPIView(APIView):
    def get(self, request):
        usuario = getattr(request.user, "username", "Anónimo")
        fabricantes = Fabricante.objects.all()
        serializer = FabricanteSerializer(fabricantes, many=True)
        return Response(serializer.data)

    def post(self, request):
        usuario = getattr(request.user, "username", "Anónimo")
        serializer = FabricanteSerializer(data=request.data)
        if serializer.is_valid():
            fabricante = serializer.save()
            LogUtil.registrar_log(
                modelo="Fabricante",
                operacion="CREAR",
                descripcion=f"{usuario} creó el fabricante '{fabricante.nombre}'"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FabricanteDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Fabricante.objects.get(pk=pk)
        except Fabricante.DoesNotExist:
            return None

    def get(self, request, pk):
        fabricante = self.get_object(pk)
        if not fabricante:
            return Response({"error": "Fabricante no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FabricanteSerializer(fabricante)
        return Response(serializer.data)

    def put(self, request, pk):
        usuario = getattr(request.user, "username", "Anónimo")
        fabricante = self.get_object(pk)
        if not fabricante:
            return Response({"error": "Fabricante no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FabricanteSerializer(fabricante, data=request.data)
        if serializer.is_valid():
            serializer.save()
            LogUtil.registrar_log(
                modelo="Fabricante",
                operacion="ACTUALIZAR",
                descripcion=f"{usuario} actualizó el fabricante '{fabricante.nombre}'"
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        usuario = getattr(request.user, "username", "Anónimo")
        fabricante = self.get_object(pk)
        if not fabricante:
            return Response({"error": "Fabricante no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        nombre = fabricante.nombre
        fabricante.delete()
        LogUtil.registrar_log(
            modelo="Fabricante",
            operacion="ELIMINAR",
            descripcion=f"{usuario} eliminó el fabricante '{nombre}'"
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
