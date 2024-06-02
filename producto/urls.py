from django.urls import path
from . import views
#crear vistas aqui
urlpatterns = [
    path('producto/', views.producto, name='producto'),
    path('producto/crearProducto/', views.crearProducto, name='crearProducto'),
    path('producto/edicionProducto/<int:pk>', views.edicionProducto, name='edicionProducto'),
    path('editarProducto/', views.editarProducto, name='editarProducto'),
    path('eliminarProducto/<int:pk>', views.eliminarProducto, name='eliminarProducto'),
    path('producto/verProducto/<int:pk>', views.verProducto, name='verProducto'),
    path('producto/buscarProducto/', views.buscarProducto, name='buscarProducto'),
]