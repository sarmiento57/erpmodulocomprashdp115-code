from django.urls import path
from . import views
from .views import EnviarCorreo
#crear vistas aqui
urlpatterns = [
    path('solicitudCompra/', views.solicitudCompra, name='solicitudCompra'),
    path('solicitudCompra/crearSolicitud/', views.crearSolicitud, name='crear_solicitud'),
    path('solicitudCompra/edicionSolicitud/<int:pk>', views.edicionSolicitud, name='edicion_solicitud'),
    path('editarSolicitud/', views.editarSolicitud, name='editar_solicitud'),
    path('eliminarSolicitud/<int:pk>', views.eliminarSolicitud, name='eliminarSolicitud'),
    path('solicitudCompra/detallesSolicitud/<int:pk>', views.verSolicitud, name='detalles_solicitud'),
    path('solicitudCompra/solicitudPdf/<int:pk>', views.solicitudPdf, name='solicitudPdf'),
    path('enviarCorreo/<int:pk>/', EnviarCorreo.as_view(), name='enviar_correo'),
    path('solicitudCompra/buscarSolicitud/', views.buscarSolicitud, name='buscarSolicitud'),


]