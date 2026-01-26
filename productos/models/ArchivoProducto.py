from django.db import models

class ArchivoProducto(models.Model):
    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE,
        related_name="archivos",
        null=True,
        blank=True
    )
    filename = models.CharField(max_length=255, default="", blank=True)
    key = models.TextField(blank=True)

    def __str__(self):
        return f"{self.key or 'sin_key'} - {self.filename or 'sin_filename'}"
