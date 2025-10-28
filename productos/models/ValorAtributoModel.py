from django.db import models

class ValorAtributoProducto(models.Model):
    producto = models.ForeignKey("productos.Producto", on_delete=models.CASCADE, related_name="atributos")
    atributo = models.ForeignKey("productos.Atributo", on_delete=models.CASCADE)
    
    valor_texto = models.TextField(blank=True, null=True)
    valor_numero = models.FloatField(blank=True, null=True)
    valor_fecha = models.DateField(blank=True, null=True)
    valor_booleano = models.BooleanField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.atributo.nombre}: {self.obtener_valor()}"
    
    def obtener_valor(self):
        if self.atributo.tipo_atributo == "texto":
            return self.valor_texto
        elif self.atributo.tipo_atributo == "numero":
            return self.valor_numero
        elif self.atributo.tipo_atributo == "fecha":
            return self.valor_fecha
        elif self.atributo.tipo_atributo == "booleano":
            return self.valor_booleano
