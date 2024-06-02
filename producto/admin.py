from django.contrib import admin
from .models import Producto
# Register your models here.
class ProductoAdmin(admin.ModelAdmin):
    list_filter = ["categoria_producto"]

admin.site.register(Producto, ProductoAdmin)
