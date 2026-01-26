from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from usuarios.authentication import CookieJWTAuthentication
from productos.models.ValorAtributoProductoModel import ValorAtributoProducto
from productos.serializers.ValorAtributoSerializer import ValorAtributoProductoSerializer
from utils.LogUtil import LogUtil


class ValorAtributoProductoListCreateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        valores = ValorAtributoProducto.objects.select_related('producto').all()
        serializer = ValorAtributoProductoSerializer(valores, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ValorAtributoProductoSerializer(data=request.data)
        if serializer.is_valid():
            valor = serializer.save()
            LogUtil.registrar_log(
                usuario=request.user, accion="CREAR",
                entidad="ValorAtributoProducto",
                detalle=f"Se crea valor (key='{valor.key}') para producto ID {valor.producto.id}"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValorAtributoProductoDetailAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ValorAtributoProducto.objects.select_related('producto').get(pk=pk)
        except ValorAtributoProducto.DoesNotExist:
            return None

    def get(self, request, pk):
        valor = self.get_object(pk)
        if not valor:
            return Response({"error": "Valor de atributo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ValorAtributoProductoSerializer(valor)
        return Response(serializer.data)

    def put(self, request, pk):
        valor = self.get_object(pk)
        if not valor:
            return Response({"error": "Valor de atributo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ValorAtributoProductoSerializer(valor, data=request.data)
        if serializer.is_valid():
            actualizado = serializer.save()
            LogUtil.registrar_log(
                usuario=request.user, accion="EDITAR",
                entidad="ValorAtributoProducto",
                detalle=f"Se actualiza valor (key='{actualizado.key}') para producto ID {actualizado.producto.id}"
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        valor = self.get_object(pk)
        if not valor:
            return Response({"error": "Valor de atributo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        producto_id = valor.producto.id
        key = valor.key
        valor.delete()
        LogUtil.registrar_log(
            usuario=request.user, accion="ELIMINAR",
            entidad="ValorAtributoProducto",
            detalle=f"Se elimina valor (key='{key}') del producto ID {producto_id}"
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
