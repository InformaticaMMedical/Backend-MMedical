from django.db import models
from .ProductoModel import Producto


class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="imagenes")
    filename = models.CharField(max_length=255)
    key = models.CharField(max_length=512, unique=True)
    url = models.URLField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("producto", "filename")]

    def __str__(self):
        return f"{self.producto_id} - {self.filename}"
