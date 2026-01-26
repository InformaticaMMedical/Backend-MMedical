from django.db import models

class ValorAtributoProducto(models.Model):
    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE,
        related_name="atributos"
    )
    atributo = models.ForeignKey(
        "productos.Atributo",
        on_delete=models.CASCADE,
        related_name="valores"
    )

    valor_texto = models.TextField(blank=True, null=True)
    valor_numero = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_booleano = models.BooleanField(blank=True, null=True)
    valor_fecha = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ("producto", "atributo")

    def __str__(self):
        return f"{self.producto} - {self.atributo}"
