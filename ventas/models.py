from django.db import models

class Cotizacion(models.Model):
    cliente_nombre = models.CharField(max_length=255, blank=True)
    cliente_email = models.EmailField(blank=True)
    cliente_empresa = models.CharField(max_length=255, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    enviada = models.BooleanField(default=False)

    def __str__(self):
        return f"Cotización #{self.id}"
    
