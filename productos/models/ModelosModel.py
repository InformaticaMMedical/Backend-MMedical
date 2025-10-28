from django.db import models
from productos.models.ProveedorModel import Proveedor


class Modelo(models.Model):
    nombre = models.CharField(max_length=180, unique=True, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name="modelos")

    def __str__(self):
        return f"{self.nombre} ({self.proveedor.nombre})"
