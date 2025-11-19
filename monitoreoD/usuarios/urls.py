from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'usuarios'

urlpatterns = [
    path('usuarios/vista/', views.lista_usuarios, name='usuarios_lista'),
    path('usuarios/crear/', views.crear_usuario, name='usuarios_crear'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='usuarios_editar'),
    path('usuarios/toggle-estado/<int:pk>/', views.toggle_usuario_estado, name='usuarios_toggle_estado'),
    path('usuarios/gestionar-roles/<int:pk>/', views.gestionar_roles, name='usuarios_gestionar_roles'),
    path('usuarios/detalle/<int:pk>/', views.detalle_usuario, name='usuarios_detalle'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Perfil de usuario
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('cambiar-contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
    
    # Exportación
    path('usuarios/exportar/', views.exportar_usuarios_excel, name='exportar_usuarios'),
    
    # Autenticación
    path('', views.custom_login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='usuarios/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='usuarios/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/password_reset_complete.html'), name='password_reset_complete'),
    
    # Test URLs
    path('test-productos/', views.test_productos, name='test_productos'),
    path('test-sin-decorador/', views.test_sin_decorador, name='test_sin_decorador'),
]