from django.db import models
from solicitudCompra.models import SolicitudCompra, ProductoSolicitud
from django.utils import timezone

# Create your models here.

class OrdenCompra(models.Model):
    fecha_factura = models.DateField(default=timezone.now)
    fecha_contable = models.DateField(null=True, blank=True)
    banco_receptor = models.CharField(max_length=50)
    solicitud = models.ForeignKey(SolicitudCompra, on_delete=models.CASCADE, null=True, blank=True)
    enviado = models.BooleanField(default=False)
    total_orden = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calcular_total_orden(self):
    
        productos = ProductoSolicitud.objects.filter(solicitud=self.solicitud)

        total_orden = sum(producto.total for producto in productos)
        return total_orden
    
    def save(self, *args, **kwargs):
        
        if not self.solicitud_id:
            ultima_solicitud = SolicitudCompra.objects.last()
            if ultima_solicitud:
                self.solicitud = ultima_solicitud

        self.total_orden = self.calcular_total_orden()
                
        super().save(*args, **kwargs)



class Factura(models.Model):
    diario = models.CharField(max_length=50, blank=True)
    metodo_pago = models.CharField(max_length=50, blank=True)
    cuenta_bancaria = models.CharField(max_length=50, blank=True)
    solicitud = models.ForeignKey(SolicitudCompra, on_delete=models.CASCADE, null=True, blank=True)
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, null=True, blank=True)
    factura_registrada = models.BooleanField(default=False)


    
    

    def save(self, *args, **kwargs):


        if not self.solicitud_id:
            ultima_solicitud = SolicitudCompra.objects.last()
            if ultima_solicitud:
                self.solicitud = ultima_solicitud

        if not self.orden_compra_id: 
            ultima_orden = OrdenCompra.objects.last()
            if ultima_orden:
                self.orden_compra = ultima_orden

        super().save(*args, **kwargs)
  

    


        



    