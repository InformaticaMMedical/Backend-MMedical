from django.db import models
from productos.models import Producto

class Cotizacion(models.Model):
    cliente_nombre = models.CharField(max_length=255)
    cliente_email = models.EmailField()
    cliente_empresa = models.CharField(max_length=255, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    enviada = models.BooleanField(default=False)

    def __str__(self):
        return f"Cotización #{self.id} - {self.cliente_nombre}"


class CotizacionItem(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
