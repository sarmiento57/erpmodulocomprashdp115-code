from django.urls import path
from . import views
#crear vistas aqui
urlpatterns = [
    path('proveedor/', views.proveedor, name='proveedor'),
    path('proveedor/crearProveedor/', views.crearProveedor, name='crearProveedor'),
    path('eliminarProveedor/<int:pk>', views.eliminarProveedor, name='eliminarProveedor'),
    path('proveedor/edicionProveedor/<int:pk>', views.edicionProveedor, name='edicionProveedor'),
    path('editarProveedor/', views.editarProveedor, name='editarProveedor'),
    path('proveedor/verProveedor/<int:pk>', views.verProveedor, name='verProveedor'),
    path('proveedor/buscarProveedor/', views.buscarProveedor, name='buscarProveedor'),
    
]