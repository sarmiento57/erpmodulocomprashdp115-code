from django.forms import ModelForm
from .models import Proveedor
from django import forms
import datetime

class ProveedorForm(ModelForm):
    nombre_proveedor = forms.CharField(label='Nombre del proveedor', max_length=50, required=True)
    direccion_proveedor = forms.CharField(label='Direccion del proveedor', max_length=300, required=True, widget=forms.Textarea)
    email_proveedor = forms.EmailField(label='Email del proveedor', max_length=60, required=True)
    telefono_proveedor = forms.IntegerField(label='Telefono del proveedor', required=True)
    contacto_proveedor = forms.CharField(label='Contacto del proveedor', max_length=50, required=True)
    fecha_creacion_proveedor = forms.DateTimeField(initial=datetime.datetime.now, widget=forms.DateTimeInput(attrs={'readonly': 'readonly'}), required=False)

    class Meta:
        model = Proveedor
        fields = ['nombre_proveedor', 'direccion_proveedor', 'email_proveedor', 'telefono_proveedor', 'contacto_proveedor', 'fecha_creacion_proveedor']