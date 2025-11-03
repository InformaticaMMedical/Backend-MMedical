from django.db import models

class ProductoCompatibilidad(models.Model):
    producto_principal = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE,
        related_name="compatibilidades_principales",
        null=True,
        blank=True
    )
    producto_relacionado = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE,
        related_name="compatibilidades_relacionadas",
        null=True,
        blank=True
    )
    filename = models.CharField(max_length=255, default="", blank=True)
    key = models.CharField(max_length=255, default="", blank=True)

    def __str__(self):
        if self.producto_principal and self.producto_relacionado:
            return f"{self.producto_principal.nombre} ↔ {self.producto_relacionado.nombre}"
        return self.filename or "Compatibilidad sin productos"
