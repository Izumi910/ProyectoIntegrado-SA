from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'usuarios'

urlpatterns = [
    path('usuarios/vista/', views.lista_usuarios, name='usuarios_lista'),
    path('usuarios/crear/', views.crear_usuario, name='usuarios_crear'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='usuarios_editar'),
    path('usuarios/eliminar/<int:pk>/', views.eliminar_usuario, name='usuarios_eliminar'),
    path('usuarios/detalle/<int:pk>/', views.detalle_usuario, name='usuarios_detalle'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Autenticación
    path('', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='usuarios/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='usuarios/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/password_reset_complete.html'), name='password_reset_complete'),
]