from django import forms
from .models import SolicitudCompra
from django.contrib.auth.models import User
from django.db import models
from proveedor.models import Proveedor
from producto.models import Producto
import datetime

class SolicitudCompraForm(forms.ModelForm):

    ESTADO_CHOICES = (
        ('Solicitud de compra','Solicitud de compra'),
        ('Orden de compra','Orden de compra'),
    )
    estado = forms.ChoiceField(choices=ESTADO_CHOICES, required=True)
    comprador = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    fecha_creacion = forms.DateTimeField(initial=datetime.datetime.now, widget=forms.DateTimeInput(attrs={'readonly': 'readonly'}), required=True)
    fecha_de_espera = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    proveedores = forms.ModelChoiceField(queryset=Proveedor.objects.all(), widget=forms.Select, required=True)
    productos = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = SolicitudCompra
        fields = ['estado', 'fecha_creacion', 'fecha_de_espera', 'proveedores', 'productos']

    
    

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SolicitudCompraForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['comprador'].initial = user.get_full_name()

    

    
