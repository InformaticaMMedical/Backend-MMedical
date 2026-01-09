from django.db import models
from productos.models import Producto

class Cotizacion(models.Model):
    cliente_nombre = models.CharField(max_length=255)
    cliente_email = models.EmailField()
    cliente_empresa = models.CharField(max_length=255, blank=True)

    cliente_rut = models.CharField(max_length=20, blank=True)
    region = models.CharField(max_length=100, blank=True)
    comuna = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    plazo_entrega = models.CharField(max_length=100, blank=True)
    comentarios = models.TextField(blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    enviada = models.BooleanField(default=False)

    def __str__(self):
        return f"Cotización #{self.id} - {self.cliente_nombre}"


class CotizacionItem(models.Model):
    cotizacion = models.ForeignKey(
        Cotizacion,
        on_delete=models.CASCADE,
        related_name="items"
    )
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
