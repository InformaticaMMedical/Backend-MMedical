from django.db import models

from productos.models.ModeloFabricanteModel import ModeloFabricante

class ProductoCompatibilidad(models.Model):
    producto = models.ForeignKey("productos.Producto", on_delete=models.CASCADE, related_name="compatibilidades")
    modelo = models.ForeignKey(ModeloFabricante, on_delete=models.CASCADE)