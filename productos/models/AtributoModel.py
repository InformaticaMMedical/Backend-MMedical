from django.db import models

TIPO_ATRIBUTO_CHOICES = [
    ('texto', 'Texto'),
    ('numero', 'Número'),
    ('fecha', 'Fecha'),
    ('booleano', 'Booleano'),
]

class Atributo(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_atributo = models.CharField(max_length=10, choices=TIPO_ATRIBUTO_CHOICES)
    categorias = models.ManyToManyField("productos.Categoria", blank=True)
    
    def __str__(self):
        return self.nombre
