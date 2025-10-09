from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.lista_movimientos, name='lista'),
    path('crear/', views.crear_movimiento, name='crear'),
    path('editar/<int:pk>/', views.editar_movimiento, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_movimiento, name='eliminar'),
    path('<int:pk>/', views.detalle_movimiento, name='detalle'),
]