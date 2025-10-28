from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from productos.models.ValorAtributoModel import ValorAtributoProducto
from productos.serializers.ValorAtributoSerializer import ValorAtributoProductoSerializer
from utils.LogUtil import LogUtil

class ValorAtributoProductoListCreateAPIView(APIView):
    def get(self, request):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        valores = ValorAtributoProducto.objects.all().select_related('producto', 'atributo')
        serializer = ValorAtributoProductoSerializer(valores, many=True)
        return Response(serializer.data)

    def post(self, request):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        serializer = ValorAtributoProductoSerializer(data=request.data)
        if serializer.is_valid():
            valor = serializer.save()
            LogUtil.registrar_log(
                modelo="ValorAtributoProducto",
                operacion="CREAR",
                descripcion=f"{usuario} creó valor de atributo para producto {valor.producto.id} y atributo {valor.atributo.id}"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValorAtributoProductoDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return ValorAtributoProducto.objects.get(pk=pk)
        except ValorAtributoProducto.DoesNotExist:
            return None

    def get(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        valor = self.get_object(pk)
        if not valor:
            return Response({"error": "Valor de atributo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ValorAtributoProductoSerializer(valor)
        return Response(serializer.data)

    def put(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        valor = self.get_object(pk)
        if not valor:
            return Response({"error": "Valor de atributo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ValorAtributoProductoSerializer(valor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            LogUtil.registrar_log(
                modelo="ValorAtributoProducto",
                operacion="ACTUALIZAR",
                descripcion=f"{usuario} actualizó valor de atributo para producto {valor.producto.id} y atributo {valor.atributo.id}"
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        usuario = request.user.username if hasattr(request.user, "username") else "Anónimo"
        valor = self.get_object(pk)
        if not valor:
            return Response({"error": "Valor de atributo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        descripcion = f"{usuario} eliminó valor de atributo para producto {valor.producto.id} y atributo {valor.atributo.id}"
        valor.delete()
        LogUtil.registrar_log(
            modelo="ValorAtributoProducto",
            operacion="ELIMINAR",
            descripcion=descripcion
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
