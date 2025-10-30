from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_atributo = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre
