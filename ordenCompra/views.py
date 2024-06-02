from django.shortcuts import render, redirect
from .models import OrdenCompra, Factura
from .forms import OrdenCompraForm, FacturaForm
from solicitudCompra.models import SolicitudCompra, ProductoSolicitud
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View
from django.core.mail import EmailMultiAlternatives
from django.conf import settings





@permission_required('ordenCompra.view_ordencompra')
def ordenCompra(request):
    solicitudes = SolicitudCompra.objects.filter(Q(estado="Orden de compra") | Q(estado="Facturado")).prefetch_related('proveedores').all()
    ordenes = OrdenCompra.objects.all()
    subtotales = [(solicitud.id, sum(producto_solicitud.subtotal for producto_solicitud in solicitud.productosolicitud_set.all())) for solicitud in solicitudes]
    return render(request, 'ordenCompra.html', {'solicitudes': solicitudes, 'ordenes': ordenes, 'subtotales': subtotales})





@permission_required('ordenCompra.add_ordencompra')
def generarPago(request, orden_id):
    orden = get_object_or_404(OrdenCompra, id=orden_id)
    factura = Factura.objects.filter(orden_compra=orden).first()
    solicitud = orden.solicitud
    productos = ProductoSolicitud.objects.filter(solicitud=solicitud)

    if request.method == 'POST':
        form = OrdenCompraForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            all_received = True
            for producto in productos:
                cantidad_recibida = int(request.POST.get(f'cantidad_recibida_{producto.id}', 0))
                impuesto = float(request.POST.get(f'impuesto_{producto.id}', 0)) 
                precio = producto.producto.precio_producto
                total = (precio * cantidad_recibida) + ((impuesto / 100) * (precio * cantidad_recibida))
                producto.cantidad_recibida = cantidad_recibida
                producto.impuesto = impuesto
                producto.total = total
                print(total)
                producto.save()

                if producto.cantidad_recibida != producto.cantidad:
                    all_received = False
            orden.enviado = True
            orden.save()
            messages.success(request, 'Orden de compra confirmada con éxito')
            return HttpResponseRedirect(reverse('generarPago', kwargs={'orden_id': orden_id}))  

    else:
        form = OrdenCompraForm(instance=orden)
    
    proveedor = solicitud.proveedores if solicitud and solicitud.proveedores else None
    proveedor_data = {
        'nombre_proveedor': proveedor.nombre_proveedor if proveedor else None,
        'contacto_proveedor': proveedor.contacto_proveedor if proveedor else None,
        'telefono_proveedor': proveedor.telefono_proveedor if proveedor else None,
        'email_proveedor': proveedor.email_proveedor if proveedor else None,
    }
    

    return render(request, 'generarPago.html', {'form': form,'orden': orden,'factura': factura,'solicitud': solicitud,'proveedor': proveedor_data,'productos': productos})




@permission_required('ordenCompra.add_ordencompra')
def factura(request, orden_id):
    orden = get_object_or_404(OrdenCompra, id=orden_id)
    factura = Factura.objects.filter(orden_compra=orden).first()
    if request.method == 'POST':
        form = FacturaForm(request.POST, instance=factura)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.orden_compra = orden
            factura.factura_registrada = True
            factura.save()

            if orden.solicitud.estado:
                orden.solicitud.estado = 'Facturado'
                orden.solicitud.save()
            messages.success(request, 'Registro confirmado con éxito')
            return HttpResponseRedirect(reverse('generarPago', kwargs={'orden_id': orden_id}))
        
    else:

        form = FacturaForm(instance=factura)
    return render(request, 'crearFactura.html', {'form': form, 'orden': orden, 'factura': factura})


@permission_required('ordenCompra.view_ordencompra')
def verOrden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, id=orden_id)
    factura = Factura.objects.filter(orden_compra=orden).first()
    solicitud = orden.solicitud
    proveedor = solicitud.proveedores if solicitud and solicitud.proveedores else None
    proveedor_data = {
        'nombre_proveedor': proveedor.nombre_proveedor if proveedor else None,
        'contacto_proveedor': proveedor.contacto_proveedor if proveedor else None,
        'telefono_proveedor': proveedor.telefono_proveedor if proveedor else None,
        'email_proveedor': proveedor.email_proveedor if proveedor else None,
    }
    return render(request, 'verOrden.html', {'orden': orden, 'factura': factura, 'solicitud': solicitud, 'proveedor': proveedor_data})


@permission_required('ordenCompra.view_ordencompra')
def facturaPdf(request, orden_id):
    orden = get_object_or_404(OrdenCompra, id=orden_id)
    factura = Factura.objects.filter(orden_compra=orden).first()
    solicitud = orden.solicitud
    proveedor = solicitud.proveedores if solicitud and solicitud.proveedores else None
    proveedor_data = {
        'nombre_proveedor': proveedor.nombre_proveedor if proveedor else None,
        'contacto_proveedor': proveedor.contacto_proveedor if proveedor else None,
        'telefono_proveedor': proveedor.telefono_proveedor if proveedor else None,
        'email_proveedor': proveedor.email_proveedor if proveedor else None,
    }
    template = get_template('facturaPdf.html')
    context = {'orden': orden, 'factura': factura, 'solicitud': solicitud, 'proveedor': proveedor_data}
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=factura_{orden.id}.pdf'
    pisaStatus = pisa.CreatePDF(html, dest=response)
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


class Send(View):
    def get(self, request, orden_id):
        return redirect('generarPago', orden_id=orden_id)

    def post(self, request, orden_id): 
        email = request.POST.get('email')
        print(email)

        orden = get_object_or_404(OrdenCompra, id=orden_id)
        factura = Factura.objects.filter(orden_compra=orden).first()
        solicitud = orden.solicitud
        proveedor = solicitud.proveedores if solicitud and solicitud.proveedores else None
        proveedor_data = {
            'nombre_proveedor': proveedor.nombre_proveedor if proveedor else None,
            'contacto_proveedor': proveedor.contacto_proveedor if proveedor else None,
            'telefono_proveedor': proveedor.telefono_proveedor if proveedor else None,
            'email_proveedor': proveedor.email_proveedor if proveedor else None,
        }

        template = get_template('facturaPdf.html')
        content = template.render({'orden': orden, 'factura': factura, 'solicitud': solicitud, 'proveedor': proveedor_data})

        msg = EmailMultiAlternatives(
            'Gracias por su envio',
            'Hola, te enviamos un correo con tu factura',
            settings.EMAIL_HOST_USER,
            [email]
        )
        msg.attach_alternative(content, 'text/html')
        msg.send()

        return redirect('generarPago', orden_id=orden_id)
    

@permission_required('ordenCompra.view_ordencompra')
def buscarOrdenCompra(request):
    query = request.GET.get('q')
    en_orden_compra = request.path.startswith('/ordenCompra/')
    
    if query:
        solicitudes = SolicitudCompra.objects.filter(
            Q(estado="Orden de compra") | Q(estado="Facturado")
        ).prefetch_related('proveedores').filter(
            Q(referencia__icontains=query) | Q(estado__icontains=query)
        )
        ordenes = OrdenCompra.objects.all()
        subtotales = [
            (solicitud.id, sum(producto_solicitud.subtotal for producto_solicitud in solicitud.productosolicitud_set.all()))
            for solicitud in solicitudes
        ]
    else:
        solicitudes = SolicitudCompra.objects.filter(
            Q(estado="Orden de compra") | Q(estado="Facturado")
        ).prefetch_related('proveedores').all()
        ordenes = OrdenCompra.objects.all()
        subtotales = [
            (solicitud.id, sum(producto_solicitud.subtotal for producto_solicitud in solicitud.productosolicitud_set.all()))
            for solicitud in solicitudes
        ]

    return render(request, 'ordenCompra.html', {'solicitudes': solicitudes,'ordenes': ordenes,'subtotales': subtotales,'en_orden_compra': en_orden_compra,})

