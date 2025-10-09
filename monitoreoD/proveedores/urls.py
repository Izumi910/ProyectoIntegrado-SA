from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
    path('', views.lista_proveedores, name='lista'),
    path('crear/', views.crear_proveedor, name='crear'),
    path('editar/<int:pk>/', views.editar_proveedor, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_proveedor, name='eliminar'),
    path('<int:pk>/', views.detalle_proveedor, name='detalle'),
]