from django.contrib import admin
from .models import OrdenCompra, Factura

# Register your models here.

admin.site.register(OrdenCompra)
admin.site.register(Factura)