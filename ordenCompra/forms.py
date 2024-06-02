from django import forms
from .models import OrdenCompra, Factura
from solicitudCompra.models import SolicitudCompra

class OrdenCompraForm(forms.ModelForm):
    fecha_factura = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type': 'date' ,'required': 'required'}))
    fecha_contable = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type': 'date', 'required': 'required'}))
    banco_receptor = forms.CharField(max_length=50, required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))
    solicitud = forms.ModelChoiceField(queryset=SolicitudCompra.objects.all(),widget=forms.Select(attrs={'class': 'form-select', 'disabled': 'disabled'}))

    class Meta:
        model = OrdenCompra
        fields = ['fecha_factura', 'fecha_contable', 'banco_receptor', 'solicitud']






class FacturaForm(forms.ModelForm):
    DIARIO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Banco', 'Banco'),
    ]
    METODO_PAGO = [
        ('Manual', 'Manual'),
        ('Transferencia', 'Transferencia')
    ]
    
    diario = forms.ChoiceField(choices=DIARIO_CHOICES,widget=forms.Select(attrs={'class': 'form-select'}))
    metodo_pago = forms.ChoiceField(choices=METODO_PAGO,widget=forms.Select(attrs={'class': 'form-select'}))
    cuenta_bancaria = forms.CharField(max_length=50,required=False,widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    solicitud = forms.ModelChoiceField(queryset=SolicitudCompra.objects.all(),widget=forms.Select(attrs={'class': 'form-select', 'disabled': 'disabled'})
    )

    class Meta:
        model = Factura
        fields = ['diario', 'metodo_pago', 'solicitud', 'cuenta_bancaria']

        




       

    