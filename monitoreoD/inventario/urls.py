from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.lista_movimientos, name='inventario_lista'),
    path('crear/', views.crear_movimiento, name='inventario_crear'),
    path('editar/<int:pk>/', views.editar_movimiento, name='inventario_editar'),

    path('<int:pk>/', views.detalle_movimiento, name='inventario_detalle'),
    path('exportar/', views.exportar_inventario_excel, name='exportar_inventario'),
]