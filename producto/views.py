from django.shortcuts import render, redirect, reverse
from .models import Producto
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from .forms import ProductoForm
from django.http import JsonResponse

@permission_required('producto.view_producto')
def producto(request):#retorna la lista de productos
    productosListado = Producto.objects.all()#retorna listado de los productos

    return render(request, 'producto.html', {'productos': productosListado})

@permission_required('producto.add_producto')
def crearProducto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, 'Producto creado correctamente')
            return redirect(reverse('producto'))
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Devolver errores del formulario en un formato adecuado para el JavaScript
                errors = {field: error[0] for field, error in form.errors.items()}
                return JsonResponse({'success': False, 'errors': errors})
    else:
        form = ProductoForm()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'crearProducto.html', {'form': form})
    return render(request, 'crearProducto.html', {'form': form})


@permission_required('producto.change_producto')
def edicionProducto(request, pk): 
    producto = Producto.objects.get(pk=pk)
    data = {
        'titulo': 'Modificando producto',
        'producto': producto
    }
    return render(request, 'modificarProducto.html', data)

@permission_required('producto.change_producto')
def editarProducto(request):
    
    id = int(request.POST['id']) #obtiene el id del producto

    nombre_producto = request.POST['nombre_producto']#obtiene el nombre del producto
    stock_producto = request.POST['stock_producto']
    categoria_producto = request.POST['categoria_producto']
    precio_producto = request.POST['precio_producto']
    descripcion_producto = request.POST['descripcion_producto']

    producto = Producto.objects.get(id=id)#obtiene el proveedor por el id

    producto.nombre_producto = nombre_producto#modifica el nombre del producto
    producto.stock_producto = stock_producto
    producto.categoria_producto= categoria_producto
    producto.precio_producto = precio_producto
    producto.descripcion_producto = descripcion_producto
    producto.save()

    messages.success(request, 'Producto modificado correctamente')

    return redirect('producto')

@permission_required('producto.delete_producto')
def eliminarProducto(request, pk): #elimina un producto
# pk es el parámetro que representa la clave primaria del producto que se desea eliminar
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    
    messages.success(request, 'Producto eliminado correctamente')

    return redirect('producto')

@permission_required('producto.view_producto')
def verProducto(request, pk):
    producto = Producto.objects.get(pk=pk)
    data = {
        'titulo': 'Detalles del producto',
        'producto': producto
    }
    return render(request, 'verProducto.html', data)

@permission_required('producto.view_producto')
def buscarProducto(request):
    query = request.GET.get('q')
    en_producto = request.path.startswith('/producto/') 
    if query:
        productosListado = Producto.objects.filter(nombre_producto__icontains=query) | Producto.objects.filter(categoria_producto__icontains=query)
    else:
        productosListado = Producto.objects.all()
    
    return render(request, 'producto.html', {'productos': productosListado, 'en_producto': en_producto})