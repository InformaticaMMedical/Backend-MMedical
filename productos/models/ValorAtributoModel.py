from django.db import models

class ValorAtributoProducto(models.Model):
    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE,
        related_name="valores_atributo"
    )
    filename = models.CharField(max_length=255)
    key = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.key} - {self.filename}"
