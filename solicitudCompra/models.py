from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from proveedor.models import Proveedor
from producto.models import Producto

class SolicitudCompra(models.Model):
  
   
    estado = models.CharField(max_length=50, blank=False)
    comprador = models.CharField(max_length=100, blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_de_espera = models.DateField(null=True, blank=True)
    proveedores = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    referencia = models.CharField(max_length=10, blank=True)
    productos = models.ManyToManyField(Producto, blank=False)

    
    def __str__(self):
        if self.referencia:
            return self.referencia
        
    def save(self, *args, **kwargs):
        if not self.referencia:
            last_solicitud = SolicitudCompra.objects.all().order_by('id').last()
            if not last_solicitud:
                self.referencia = 'P0000'
            else:
                last_ref = last_solicitud.referencia
                if last_ref:
                    last_ref_int = int(last_ref[1:])
                else:
                    last_ref_int = 0
                new_ref_int = last_ref_int + 1
                self.referencia = f'P{new_ref_int:04d}'
        super().save(*args, **kwargs)





class ProductoSolicitud(models.Model):
    solicitud = models.ForeignKey(SolicitudCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=100, blank=True)
    cantidad_recibida = models.IntegerField(blank=True, null=True)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.producto.descripcion_producto} - {self.producto.nombre_producto} - {self.solicitud.referencia}'
    
  