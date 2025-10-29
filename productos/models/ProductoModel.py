from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    
    categoria = models.ForeignKey(
        "productos.Categoria",
        on_delete=models.CASCADE,
        related_name="productos"
    )
    
    proveedores = models.ManyToManyField(
        "productos.Proveedor",
        blank=True,
        related_name="productos"
    )

    modelos_compatibles = models.ManyToManyField(
        "productos.ModeloFabricante",
        through="productos.ProductoCompatibilidad",
        related_name="productos_compatibles"
    )

    def __str__(self):
        return self.nombre
