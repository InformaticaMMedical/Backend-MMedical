from django.db import models
from productos.models.FabricanteModel import Fabricante

class ModeloFabricante(models.Model):
    nombre = models.CharField(max_length=150)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE, related_name="modelos")

    def __str__(self):
        return f"{self.nombre} ({self.fabricante.nombre})"
