from django.db import models

class ImagenProducto(models.Model):
    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE,
        related_name="imagenes"
    )
    filename = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.filename} ({self.producto.nombre})"
