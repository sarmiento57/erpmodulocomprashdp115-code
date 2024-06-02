from django.shortcuts import render, redirect, reverse
from .models import Proveedor
from .forms import ProveedorForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

#crea tus vistas aqui

@permission_required('proveedor.view_proveedor')
def proveedor(request):
    proveedoresListado = Proveedor.objects.all()

    return render(request, 'proveedor.html', {'proveedores': proveedoresListado})



@permission_required('proveedor.add_proveedor')
def crearProveedor(request): #crea un nuevo proveedor
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            nuevoProveedor = form.save(commit=False)
            nuevoProveedor.save()
            messages.success(request, 'Proveedor creado correctamente')
            return redirect(reverse('proveedor'),
                {'form': form})
    else:
        form = ProveedorForm()
    return render(request, 'crearProveedor.html', {'form': form})

@permission_required('proveedor.view_proveedor')
def edicionProveedor(request, pk): 
    proveedor = Proveedor.objects.get(pk=pk)
    data = {
        'titulo': 'Modificando proveedor',
        'proveedor': proveedor
    }
    return render(request, 'modificarProveedor.html', data)

@permission_required('proveedor.change_proveedor')
def editarProveedor(request):
    
    id = int(request.POST['id']) #obtiene el id del proveedor

    nombre_proveedor = request.POST['nombre_proveedor']#obtiene el nombre del proveedor
    direccion_proveedor = request.POST['direccion_proveedor']
    email_proveedor = request.POST['email_proveedor']

    proveedor = Proveedor.objects.get(id=id)#obtiene el proveedor por el id

    proveedor.nombre_proveedor = nombre_proveedor#modifica el nombre del proveedor
    proveedor.direccion_proveedor = direccion_proveedor
    proveedor.email_proveedor = email_proveedor
    proveedor.save()

    messages.success(request, 'Proveedor modificado correctamente')

    return redirect('proveedor')
    
@permission_required('proveedor.delete_proveedor')
def eliminarProveedor(request, pk): #elimina un proveedor
# pk es el parámetro que representa la clave primaria del proveedor que se desea eliminar
    proveedor = get_object_or_404(Proveedor, pk=pk)
    proveedor.delete()
    
    messages.success(request, 'Proveedor eliminado correctamente')

    return redirect('proveedor')

def verProveedor(request, pk):
    proveedor = Proveedor.objects.get(pk=pk)
    data = {
        'titulo': 'Detalles del proveedor',
        'proveedor': proveedor
    }
    return render(request, 'verProveedor.html', data)
    

@permission_required('proveedor.view_proveedor')
def buscarProveedor(request):
    query = request.GET.get('q') 
    en_proveedor = request.path.startswith('/proveedor/')
    if query:
        proveedoresListado = Proveedor.objects.filter(nombre_proveedor__icontains=query) | Proveedor.objects.filter(contacto_proveedor__icontains=query)
        
    else:
        proveedoresListado = Proveedor.objects.all()

    
    return render(request, 'proveedor.html', {'proveedores': proveedoresListado, 'en_proveedor': en_proveedor})