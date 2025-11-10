from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
    path('', views.lista_proveedores, name='proveedores_lista'),
    path('crear/', views.crear_proveedor, name='proveedores_crear'),
    path('editar/<int:pk>/', views.editar_proveedor, name='proveedores_editar'),
    path('toggle-estado/<int:pk>/', views.toggle_proveedor_estado, name='proveedores_toggle_estado'),
    path('<int:pk>/', views.detalle_proveedor, name='proveedores_detalle'),
    path('exportar/', views.exportar_proveedores_excel, name='exportar_proveedores'),
]