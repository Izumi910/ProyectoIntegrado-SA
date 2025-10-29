from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('vista/', views.lista_productos, name='productos_lista'),
    path('crear/', views.crear_producto, name='producto_crear'),
    path('editar/<int:pk>/', views.editar_producto, name='producto_editar'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='producto_eliminar'),
    path('detalle/<int:pk>/', views.detalle_producto, name='producto_detalle'),
    path('producto/<int:pk>/', views.detalle_producto, name='producto'),
    path('panel/', views.panel_productos, name='panel_productos'),
]