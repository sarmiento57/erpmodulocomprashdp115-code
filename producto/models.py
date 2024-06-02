from django.db import models

# Create your models here.
class Producto(models.Model):
        nombre_producto = models.CharField( max_length=50, blank=False)
        stock_producto = models.IntegerField( blank=False)
        categoria_producto = models.CharField(max_length=100, blank=False)
        precio_producto = models.FloatField(blank=False)
        descripcion_producto = models.CharField(max_length=150, blank=False)
           

        def __str__(self):
            return self.nombre_producto

