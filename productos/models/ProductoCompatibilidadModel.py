from django.db import models

class ProductoCompatibilidad(models.Model):
    producto_principal = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE,
        related_name="compatibilidades_principales"
    )
    producto_relacionado = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE,
        related_name="compatibilidades_relacionadas"
    )
    filename = models.CharField(max_length=255)
    key = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.producto_principal.nombre} ↔ {self.producto_relacionado.nombre}"
