from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
    path('', views.lista_proveedores, name='proveedores_lista'),
    path('crear/', views.crear_proveedor, name='proveedores_crear'),
    path('editar/<int:pk>/', views.editar_proveedor, name='proveedores_editar'),
    path('eliminar/<int:pk>/', views.eliminar_proveedor, name='proveedores_eliminar'),
    path('<int:pk>/', views.detalle_proveedor, name='proveedores_detalle'),
]