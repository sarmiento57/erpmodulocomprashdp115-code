from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import SolicitudCompra, ProductoSolicitud
from .forms import SolicitudCompraForm
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from proveedor.models import Proveedor
from ordenCompra.models import OrdenCompra, Factura
from producto.models import Producto
from django.shortcuts import get_object_or_404
import json
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.views import View



@permission_required('solicitudCompra.view_solicitudcompra')
def solicitudCompra(request):
    solicitudListado = SolicitudCompra.objects.prefetch_related('proveedores').all()
    return render(request, 'solicitud.html', {'solicitudes': solicitudListado})

@permission_required('solicitudCompra.add_solicitudcompra')
def crearSolicitud(request):
    productos_lista = Producto.objects.all()
    if request.method == 'POST':
        form = SolicitudCompraForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            full_name = f"{request.user.first_name} {request.user.last_name}"
            solicitud.comprador = full_name
            solicitud.save()

          
            productos_json = request.POST.get('productos')
            productos_seleccionados = json.loads(productos_json)

      
            for producto_data in productos_seleccionados:
                producto_id = producto_data['id']
                producto = Producto.objects.get(id=producto_id)
                cantidad = producto_data['cantidad']
                subtotal = producto.precio_producto * cantidad
                categoria = producto.categoria_producto
          

                if producto.stock_producto >= cantidad:
                    producto.stock_producto -= cantidad
                    producto.save()

                
            
                ProductoSolicitud.objects.create(
                    solicitud=solicitud,
                    producto=producto,
                    cantidad=cantidad,
                    subtotal=subtotal,
                    categoria=categoria
                
                )
            else: 
                messages.error(request, f'No hay suficiente stock para el producto {producto.nombre_producto}')

          
            nueva_orden_compra = OrdenCompra.objects.create()
            solicitud.orden_compra = nueva_orden_compra

          
            nueva_factura = Factura.objects.create()
            solicitud.factura = nueva_factura

     
            solicitud.save()

            messages.success(request, 'Solicitud creada con éxito')
            return redirect(reverse('solicitudCompra'))
        else:
            print("El formulario no es válido")
            print(form.errors)

    else:
        form = SolicitudCompraForm(user=request.user)

    return render(request, 'crearSolicitud.html', {'form': form, 'productos_lista': productos_lista})


@permission_required('solicitudCompra.change_solicitudcompra')
def edicionSolicitud(request, pk):
    solicitudCompra = get_object_or_404(SolicitudCompra, pk=pk)
    solicitudCompra.fecha_de_espera = solicitudCompra.fecha_de_espera.strftime('%Y-%m-%d')
    proveedores = Proveedor.objects.all()
    productos_lista = Producto.objects.all()

    productos_seleccionados = ProductoSolicitud.objects.filter(solicitud=solicitudCompra)

    productos_seleccionados = [
        {
            'id': producto.producto.id,
            'nombre': producto.producto.nombre_producto,
            'descripcion': producto.producto.descripcion_producto,
            'precio': float(producto.producto.precio_producto),
            'cantidad': producto.cantidad,
            'subtotal': float(producto.subtotal),
            'categoria': producto.producto.categoria_producto,
            'stock': producto.producto.stock_producto
        }
        for producto in productos_seleccionados
    ]

    data = {
        'titulo': 'Editar solicitud',
        'solicitudCompra': solicitudCompra,
        'proveedores': proveedores,
        'productos_lista': productos_lista,
        'productos_seleccionados': json.dumps(productos_seleccionados)
    }
    return render(request, 'modificarSolicitud.html', data)

@permission_required('solicitudCompra.change_solicitudcompra')
def editarSolicitud(request):
    id = int(request.POST['id'])

    estado = request.POST['estado']
    fecha_de_espera = request.POST['fecha_de_espera']
    proveedores = request.POST['proveedores']

    solicitudCompra = SolicitudCompra.objects.get(id=id)

    solicitudCompra.estado = estado
    solicitudCompra.fecha_de_espera = fecha_de_espera
    solicitudCompra.fecha_actualizacion = timezone.now()
    solicitudCompra.proveedores = Proveedor.objects.get(id=proveedores)
    solicitudCompra.save()

    productos_json = request.POST.get('productos')
    productos_seleccionados = json.loads(productos_json)

    for producto_data in productos_seleccionados:
        producto_id = producto_data['id']
        producto = Producto.objects.get(id=producto_id)
        cantidad = producto_data['cantidad']
        subtotal = producto.precio_producto * cantidad
        categoria = producto.categoria_producto

        if producto.stock_producto >= cantidad:
            producto.stock_producto -= cantidad
            producto.save()

        ProductoSolicitud.objects.update_or_create(
            solicitud=solicitudCompra,
            producto=producto,
            defaults={
                'cantidad': cantidad,
                'subtotal': subtotal,
                'categoria': categoria
            }
        )
    else:
        messages.error(request, 'No hay suficiente stock para algunos productos')

    messages.success(request, 'Solicitud actualizada con éxito')
    return redirect('solicitudCompra')

@permission_required('solicitudCompra.delete_solicitudcompra')
def eliminarSolicitud(request, pk):
    solicitudCompra = SolicitudCompra.objects.get(pk=pk)
    solicitudCompra.delete()
    messages.success(request, 'Solicitud eliminada con éxito')
    return redirect('solicitudCompra')


@permission_required('solicitudCompra.view_solicitudcompra')
def verSolicitud(request, pk):
    solicitudCompra = get_object_or_404(SolicitudCompra, pk=pk)
    data = {
        'titulo': 'Detalles de la solicitud',
        'solicitudCompra': solicitudCompra,
        'pk': pk, 
    }
    solicitud_pdf_url = reverse('solicitudPdf', kwargs={'pk': pk})
    data['solicitud_pdf_url'] = solicitud_pdf_url 
    return render(request, 'verSolicitud.html', data)

@permission_required('solicitudCompra.view_solicitudcompra')
def solicitudPdf(request, pk):
    solicitudCompra = SolicitudCompra.objects.get(pk=pk)
    productos = ProductoSolicitud.objects.filter(solicitud=solicitudCompra)
    data = {
        'solicitudCompra': solicitudCompra,
        'productos': productos
    }
    template = get_template('solicitudPdf.html')
    html = template.render(data)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=solicitud_{solicitudCompra.id}.pdf'
    pisaStatus = pisa.CreatePDF(html, dest=response)
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@permission_required('solicitudCompra.view_solicitudcompra')
def buscarSolicitud(request):
    query = request.GET.get('q')
    en_solicitud = request.path.startswith('/solicitudCompra/')
    
    if query:
        solicitudListado = SolicitudCompra.objects.filter(estado__icontains=query).prefetch_related('proveedores')
    else:
        solicitudListado = SolicitudCompra.objects.prefetch_related('proveedores').all()

    return render(request, 'solicitud.html', {'solicitudes': solicitudListado, 'en_solicitud': en_solicitud})

class EnviarCorreo(View):
    def get(self, request, pk):
        return redirect('detalles_solicitud', pk=pk)

    def post(self, request, pk): 
        email = request.POST.get('email')
        print(email)

        solicitudCompra = get_object_or_404(SolicitudCompra, pk=pk)
        data = {
        'titulo': 'Detalles de la solicitud',
        'solicitudCompra': solicitudCompra,
        'pk': pk, 
        }

        template = get_template('solicitudPdf.html')
        content = template.render(data)  

        msg = EmailMultiAlternatives(
            'Estimado proveedor,',
            'Espero que se encuentre bien. Le escribo en relación a la solicitud de compra que adjunto en este correo. Quedo atento a su respuesta. Saludos cordiales.',
            settings.EMAIL_HOST_USER,
            [email]
        )
        msg.attach_alternative(content, 'text/html')
        msg.send()

        return redirect('detalles_solicitud', pk=pk)


