from django.forms import ModelForm
from .models import Producto
from django import forms


class ProductoForm(ModelForm):
    CATEGORIA_PRODUCTO_CHOICES = (
        ('Herramienta','Herramienta'),
        ('Material','Material'),
        ('Productos químicos','Productos químicos'),
        ('Electrodomésticos','Electrodomésticos'),
        ('Muebles','Muebles'),
        ('Productos electrónicos de consumo','Productos electrónicos de consumo'),
        ('Artículos para el hogar','Artículos para el hogar'),
        ('Otros','Otros')
    )
    
    nombre_producto = forms.CharField(label='Nombre del producto',max_length=50, required=True)
    stock_producto = forms.IntegerField(label='Stock del producto',required=True)
    categoria_producto = forms.ChoiceField(label='Categoria del producto',choices=CATEGORIA_PRODUCTO_CHOICES, required=True, widget=forms.Select())
    precio_producto = forms.FloatField(label='Precio del producto', required=True)
    descripcion_producto = forms.CharField(label='Descripcion del producto',max_length=150, required=True)
    
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'stock_producto', 'categoria_producto', 'precio_producto', 'descripcion_producto']