from django.db import models
from django.utils import timezone

# Create your models here.
class Proveedor(models.Model):
        nombre_proveedor = models.CharField( max_length=50, blank=False)
        contacto_proveedor = models.CharField( max_length=50, blank=False)
        direccion_proveedor = models.CharField(max_length=300, blank=False)
        email_proveedor = models.EmailField(max_length=60, blank=False)
        telefono_proveedor = models.IntegerField(blank=False)
        fecha_creacion_proveedores = models.DateTimeField(default=timezone.now)
        
           

        def __str__(self):
            return self.nombre_proveedor
