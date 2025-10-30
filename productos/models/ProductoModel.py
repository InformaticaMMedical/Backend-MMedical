from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(
        "productos.Categoria",
        on_delete=models.CASCADE,
        related_name="productos"
    )
    proveedores = models.ManyToManyField("productos.Proveedor", blank=True)
    modelo_fabricante = models.ForeignKey(
        "productos.ModeloFabricante",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos"
    )

    def __str__(self):
        return self.nombre
