from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('vista/', views.lista_productos, name='lista'),
    path('crear/', views.crear_producto, name='crear'),
    path('editar/<int:pk>/', views.editar_producto, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar'),
    path('detalle/<int:pk>/', views.detalle_producto, name='detalle'),
    path('producto/<int:pk>/', views.detalle_producto, name='producto'),
    path('panel/', views.panel_productos, name='panel_productos'),
]