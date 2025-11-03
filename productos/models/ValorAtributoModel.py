from django.db import models

class ValorAtributoProducto(models.Model):
    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE,
        related_name="valores_atributo",
        null=True,
        blank=True
    )
    filename = models.CharField(max_length=255, default="", blank=True)
    key = models.CharField(max_length=255, default="", blank=True)

    def __str__(self):
        return f"{self.key or 'sin_key'} - {self.filename or 'sin_filename'}"
