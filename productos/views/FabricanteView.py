####################################################################################################
# Desarrollador:         Gonzalo Tapia
# Fecha:                 30-10-2025
# URL dev listado:       http:localhost:8000/productos/fabricantes/
# URL dev CRUD:          http:localhost:8000/productos/fabricantes/<int:pk>/
# URL prod:
####################################################################################################

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from usuarios.authentication import CookieJWTAuthentication
from productos.models.FabricanteModel import Fabricante
from productos.serializers.FabricanteSerializer import FabricanteSerializer
from utils.LogUtil import LogUtil


class FabricanteListCreateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fabricantes = Fabricante.objects.all()
        serializer = FabricanteSerializer(fabricantes, many=True)

        LogUtil.registrar_log(
            usuario=request.user,
            accion="CONSULTAR",
            entidad="Fabricante",
            detalle="Se consulta la lista de fabricantes"
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = FabricanteSerializer(data=request.data)
        if serializer.is_valid():
            fabricante = serializer.save()

            LogUtil.registrar_log(
                usuario=request.user,
                accion="CREAR",
                entidad="Fabricante",
                detalle=f"Se crea el fabricante '{fabricante.nombre}'"
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FabricanteDetailAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

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

        LogUtil.registrar_log(
            usuario=request.user,
            accion="CONSULTAR",
            entidad="Fabricante",
            detalle=f"Se consulta el fabricante '{fabricante.nombre}'"
        )

        return Response(serializer.data)

    def put(self, request, pk):
        fabricante = self.get_object(pk)
        if not fabricante:
            return Response({"error": "Fabricante no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FabricanteSerializer(fabricante, data=request.data)
        if serializer.is_valid():
            fabricante_actualizado = serializer.save()

            LogUtil.registrar_log(
                usuario=request.user,
                accion="EDITAR",
                entidad="Fabricante",
                detalle=f"Se actualiza el fabricante '{fabricante_actualizado.nombre}'"
            )

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        fabricante = self.get_object(pk)
        if not fabricante:
            return Response({"error": "Fabricante no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        nombre = fabricante.nombre
        fabricante.delete()

        LogUtil.registrar_log(
            usuario=request.user,
            accion="ELIMINAR",
            entidad="Fabricante",
            detalle=f"Se elimina el fabricante '{nombre}'"
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
