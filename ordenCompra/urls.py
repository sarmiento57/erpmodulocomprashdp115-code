from django.urls import path
from . import views
from .views import Send

urlpatterns = [
    path('ordenCompra/', views.ordenCompra, name='ordenCompra'),
    path('ordenCompra/generarPago/<int:orden_id>/', views.generarPago, name='generarPago'),
    path('ordenCompra/generarPago/factura/<int:orden_id>/', views.factura, name='factura'),
    path('ordenCompra/verOrden/<int:orden_id>/', views.verOrden, name='verOrden'),
    path('ordenCompra/facturaPdf/<int:orden_id>/', views.facturaPdf, name='facturaPdf'),
    path('send/<int:orden_id>/', Send.as_view(), name='send_email'),
    path('ordenCompra/buscarOrdenCompra/', views.buscarOrdenCompra, name='buscarOrdenCompra'),

 
    
    
]