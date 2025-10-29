from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf import settings
from botocore.exceptions import ClientError

from productos.models.ImagenProductoModel import ImagenProducto
from productos.models.ProductoModel import Producto
from productos.serializers.ImagenProductoSerializer import ImagenProductoSerializer
from utils.SupaBaseStorage import get_s3_client, public_url_for_key


class ImagenesProductoCollectionView(APIView):

    def get(self, request, producto_id: int):
        get_object_or_404(Producto, pk=producto_id)
        qs = ImagenProducto.objects.filter(producto_id=producto_id).order_by("-created_at")
        serializer = ImagenProductoSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, producto_id: int):
        producto = get_object_or_404(Producto, pk=producto_id)
        file = request.FILES.get("archivo")
        desired_filename = request.data.get("filename") or (file.name if file else None)

        if not file:
            return Response({"detail": "No se envió ningún archivo."}, status=status.HTTP_400_BAD_REQUEST)
        if not desired_filename:
            return Response({"detail": "No se pudo determinar el nombre del archivo."}, status=status.HTTP_400_BAD_REQUEST)


        key = f"productos/{producto.id}/{desired_filename}"


        if ImagenProducto.objects.filter(producto=producto, filename=desired_filename).exists():
            return Response({"detail": "Ya existe una imagen con ese nombre en este producto."},
                            status=status.HTTP_409_CONFLICT)

        s3 = get_s3_client()
        try:
            s3.upload_fileobj(file, settings.SUPABASE_BUCKET, key)
        except ClientError as e:
            return Response({"detail": f"Error subiendo a storage: {e}"}, status=status.HTTP_502_BAD_GATEWAY)

        url = public_url_for_key(key)
        obj = ImagenProducto.objects.create(producto=producto, filename=desired_filename, key=key, url=url)
        return Response(ImagenProductoSerializer(obj).data, status=status.HTTP_201_CREATED)


class ImagenProductoDetailView(APIView):

    def delete(self, request, imagen_id: int):
        img = get_object_or_404(ImagenProducto, pk=imagen_id)
        s3 = get_s3_client()
        try:
            s3.delete_object(Bucket=settings.SUPABASE_BUCKET, Key=img.key)
        except ClientError as e:
            return Response({"detail": f"Error eliminando en storage: {e}"}, status=status.HTTP_502_BAD_GATEWAY)

        img.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, imagen_id: int):
        img = get_object_or_404(ImagenProducto, pk=imagen_id)
        nuevo_filename = request.data.get("nuevo_filename")

        if not nuevo_filename:
            return Response({"detail": "nuevo_filename es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        carpeta = f"productos/{img.producto_id}"
        new_key = f"{carpeta}/{nuevo_filename}"

        if ImagenProducto.objects.filter(producto=img.producto, filename=nuevo_filename).exclude(pk=img.pk).exists():
            return Response({"detail": "Ya existe otra imagen con ese nombre en este producto."},
                            status=status.HTTP_409_CONFLICT)

        s3 = get_s3_client()
        try:
            s3.copy_object(
                Bucket=settings.SUPABASE_BUCKET,
                CopySource=f"{settings.SUPABASE_BUCKET}/{img.key}",
                Key=new_key,
            )
            s3.delete_object(Bucket=settings.SUPABASE_BUCKET, Key=img.key)
        except ClientError as e:
            return Response({"detail": f"Error renombrando en storage: {e}"}, status=status.HTTP_502_BAD_GATEWAY)

        img.filename = nuevo_filename
        img.key = new_key
        img.url = public_url_for_key(new_key)
        img.save()

        return Response(ImagenProductoSerializer(img).data)
