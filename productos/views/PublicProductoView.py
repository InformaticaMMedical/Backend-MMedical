from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from productos.models.ProductoModel import Producto
from productos.models.CategoriaModel import Categoria
from productos.serializers.ProductoSerializer import ProductoSerializer

import unicodedata
import re


def slugify(nombre: str) -> str:
    if not nombre:
        return ""

    nombre = nombre.strip().lower()

    nombre = unicodedata.normalize("NFKD", nombre)
    nombre = "".join([c for c in nombre if not unicodedata.combining(c)])

    nombre = re.sub(r"[^a-z0-9]+", "-", nombre)

    nombre = nombre.strip("-")

    return nombre


class PublicProductoListAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        categoria = request.query_params.get("categoria")
        categoria_slug = request.query_params.get("categoria_slug")

        productos = (
            Producto.objects
            .all()
            .select_related("categoria", "modelo_fabricante")
            .prefetch_related("proveedores", "atributos", "archivos", "imagenes")
        )

        if categoria:
            productos = productos.filter(categoria__nombre__iexact=categoria)

        if categoria_slug:
            categorias = Categoria.objects.all()
            categoria_real = None

            for c in categorias:
                if slugify(c.nombre) == categoria_slug:
                    categoria_real = c.nombre
                    break

            if categoria_real:
                productos = productos.filter(categoria__nombre__iexact=categoria_real)
            else:
                productos = Producto.objects.none()

        serializer = ProductoSerializer(productos, many=True, context={"request": request})
        return Response(serializer.data)


class PublicProductoDetailAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, pk):
        try:
            producto = (
                Producto.objects
                .select_related("categoria", "modelo_fabricante")
                .prefetch_related("proveedores", "atributos", "archivos", "imagenes")
                .get(pk=pk)
            )
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=404)

        serializer = ProductoSerializer(producto, context={"request": request})
        return Response(serializer.data)
