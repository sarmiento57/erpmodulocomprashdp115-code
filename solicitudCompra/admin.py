from django.contrib import admin
from .models import SolicitudCompra, ProductoSolicitud

# Register your models here.

class SolicitudCompraAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_actualizacion',)
    list_display = ["referencia", "estado", "comprador", "fecha_creacion", "fecha_actualizacion", "fecha_de_espera", "proveedores"]
    list_filter = ["estado"]

class ProductoSolicitudAdmin(admin.ModelAdmin):
    list_filter = ["solicitud"]

 

admin.site.register(SolicitudCompra, SolicitudCompraAdmin)
admin.site.register(ProductoSolicitud, ProductoSolicitudAdmin)