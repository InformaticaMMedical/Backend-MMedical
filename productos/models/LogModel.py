from django.db import models
from django.utils import timezone

class Log(models.Model):
    ACCIONES = [
        ('AGREGAR', 'Agregar'),
        ('EDITAR', 'Editar'),
        ('ELIMINAR', 'Eliminar'),
        ('CONSULTAR', 'Consultar'),
    ]

    usuario = models.CharField(max_length=100, null=True)
    accion = models.CharField(max_length=20, choices=ACCIONES, null=True)
    entidad = models.CharField(max_length=100, null=True)
    detalle = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return f"{self.usuario} - {self.accion} - {self.entidad} ({self.fecha.strftime('%d-%m-%Y %H:%M:%S')})"
