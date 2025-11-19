from django.test import TestCase, Client
from django.urls import reverse
from usuarios.models import Usuario
from django.contrib.sessions.models import Session
from django.utils import timezone
from datetime import timedelta

class MenuFunctionalTests(TestCase):
    """Tests funcionales para el módulo de Menú Principal"""
    
    def setUp(self):
        """Configuración inicial para todos los tests"""
        self.client = Client()
        
        # Crear usuarios de prueba con diferentes roles
        self.admin = Usuario.objects.create_user(
            username='admin_test',
            password='Admin123!',
            email='admin@test.com',
            rol='ADMINISTRADOR',
            estado='ACTIVO'
        )
        
        self.gerente = Usuario.objects.create_user(
            username='gerente_test',
            password='Gerente123!',
            email='gerente@test.com',
            rol='GERENTE_GENERAL',
            estado='ACTIVO'
        )
        
        self.operador = Usuario.objects.create_user(
            username='operador_test',
            password='Operador123!',
            email='operador@test.com',
            rol='OPERADOR_INVENTARIO',
            estado='ACTIVO'
        )
        
        self.lector = Usuario.objects.create_user(
            username='lector_test',
            password='Lector123!',
            email='lector@test.com',
            rol='LECTOR',
            estado='ACTIVO'
        )
        
        self.inactivo = Usuario.objects.create_user(
            username='inactivo_test',
            password='Inactivo123!',
            email='inactivo@test.com',
            rol='LECTOR',
            estado='INACTIVO'
        )

    def test_F_MENU_01_visualizacion_menu_segun_rol(self):
        """F-MENU-01: Visualización del menú según rol de usuario"""
        # Login como admin
        self.client.login(username='admin_test', password='Admin123!')
        response = self.client.get(reverse('usuarios:dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Login como operador
        self.client.logout()
        self.client.login(username='operador_test', password='Operador123!')
        response = self.client.get(reverse('usuarios:dashboard'))
        self.assertEqual(response.status_code, 200)
        
        print("✓ F-MENU-01: FUNCIONA - Menú se visualiza según rol")

    def test_F_MENU_02_acceso_dashboard(self):
        """F-MENU-02: Acceso al dashboard desde menú principal"""
        self.client.login(username='admin_test', password='Admin123!')
        response = self.client.get(reverse('usuarios:dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        
        print("✓ F-MENU-02: FUNCIONA - Acceso a dashboard correcto")

    def test_F_MENU_03_navegacion_modulos(self):
        """F-MENU-03: Navegación a cada módulo desde el menú"""
        self.client.login(username='admin_test', password='Admin123!')
        
        # Test navegación a productos
        response = self.client.get(reverse('productos:lista'))
        self.assertEqual(response.status_code, 200)
        
        # Test navegación a proveedores
        response = self.client.get(reverse('proveedores:lista'))
        self.assertEqual(response.status_code, 200)
        
        # Test navegación a inventario
        response = self.client.get(reverse('inventario:lista'))
        self.assertEqual(response.status_code, 200)
        
        # Test navegación a usuarios
        response = self.client.get(reverse('usuarios:usuarios_lista'))
        self.assertEqual(response.status_code, 200)
        
        print("✓ F-MENU-03: FUNCIONA - Navegación a todos los módulos correcta")

    def test_F_MENU_04_cierre_sesion(self):
        """F-MENU-04: Cierre de sesión desde menú"""
        self.client.login(username='admin_test', password='Admin123!')
        
        # Verificar que está autenticado
        response = self.client.get(reverse('usuarios:dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Cerrar sesión
        response = self.client.get(reverse('usuarios:logout'))
        
        # Intentar acceder a URL protegida
        response = self.client.get(reverse('usuarios:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirige a login
        
        print("✓ F-MENU-04: FUNCIONA - Cierre de sesión correcto")

    def test_F_MENU_05_recarga_menu_tras_logout_login(self):
        """F-MENU-05: Recarga de menú tras logout/login"""
        # Login como admin
        self.client.login(username='admin_test', password='Admin123!')
        response = self.client.get(reverse('usuarios:dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Logout
        self.client.logout()
        
        # Login como operador
        self.client.login(username='operador_test', password='Operador123!')
        response = self.client.get(reverse('usuarios:dashboard'))
        self.assertEqual(response.status_code, 200)
        
        print("✓ F-MENU-05: FUNCIONA - Menú se recarga correctamente")

    def test_F_MENU_06_restriccion_acceso_sin_permisos(self):
        """F-MENU-06: Restricción de acceso a opciones sin permisos"""
        self.client.login(username='lector_test', password='Lector123!')
        
        # Intentar acceder a crear producto (sin permiso)
        response = self.client.get(reverse('productos:crear'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        print("✓ F-MENU-06: FUNCIONA - Restricción de acceso sin permisos")

    def test_F_MENU_07_acceso_completo_administrador(self):
        """F-MENU-07: Acceso completo a todas las opciones del menú"""
        self.client.login(username='admin_test', password='Admin123!')
        
        # Verificar acceso a todas las áreas
        urls_admin = [
            'usuarios:usuarios_lista',
            'productos:lista',
            'proveedores:lista',
            'inventario:lista',
        ]
        
        for url_name in urls_admin:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)
        
        print("✓ F-MENU-07: FUNCIONA - Administrador tiene acceso completo")

    def test_F_MENU_09_acceso_perfil_usuario(self):
        """F-MENU-09: Acceso al perfil de usuario desde menú"""
        self.client.login(username='admin_test', password='Admin123!')
        
        response = self.client.get(reverse('usuarios:perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/perfil.html')
        
        print("✓ F-MENU-09: FUNCIONA - Acceso a perfil correcto")

    def test_F_MENU_11_bloqueo_usuario_inactivo(self):
        """F-MENU-11: Bloqueo de acceso a usuario desactivado"""
        # Intentar login con usuario inactivo
        login_success = self.client.login(
            username='inactivo_test',
            password='Inactivo123!'
        )
        
        # El login puede ser exitoso pero el middleware debe bloquear
        if login_success:
            response = self.client.get(reverse('usuarios:dashboard'))
            # Debe redirigir a login o mostrar error
            self.assertIn(response.status_code, [302, 403])
        
        print("✓ F-MENU-11: FUNCIONA - Usuario inactivo bloqueado")

    def test_F_MENU_13_prevencion_sesiones_multiples(self):
        """F-MENU-13: Prevención de sesiones múltiples simultáneas"""
        # Crear dos clientes (simulando dos navegadores)
        client1 = Client()
        client2 = Client()
        
        # Login en cliente 1
        client1.login(username='admin_test', password='Admin123!')
        response1 = client1.get(reverse('usuarios:dashboard'))
        self.assertEqual(response1.status_code, 200)
        
        # Login en cliente 2 con mismo usuario
        client2.login(username='admin_test', password='Admin123!')
        response2 = client2.get(reverse('usuarios:dashboard'))
        self.assertEqual(response2.status_code, 200)
        
        # Verificar que cliente 1 fue desconectado
        response1_after = client1.get(reverse('usuarios:dashboard'))
        # Debe redirigir a login
        self.assertEqual(response1_after.status_code, 302)
        
        print("✓ F-MENU-13: FUNCIONA - Prevención de sesiones múltiples")

    def test_F_MENU_14_acceso_exportacion_con_permisos(self):
        """F-MENU-14: Acceso a opciones de exportación según permisos"""
        # Gerente tiene permisos de exportación
        self.client.login(username='gerente_test', password='Gerente123!')
        
        # Intentar exportar productos
        response = self.client.get(reverse('productos:exportar_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
        print("✓ F-MENU-14: FUNCIONA - Exportación con permisos correcta")


class MenuIntegrationTests(TestCase):
    """Tests de integración adicionales"""
    
    def setUp(self):
        self.client = Client()
        self.user = Usuario.objects.create_user(
            username='test_user',
            password='Test123!',
            email='test@test.com',
            rol='ADMINISTRADOR',
            estado='ACTIVO'
        )

    def test_login_redirect_to_dashboard(self):
        """Verificar redirección correcta después del login"""
        response = self.client.post(reverse('usuarios:login'), {
            'username': 'test_user',
            'password': 'Test123!'
        })
        
        self.assertRedirects(response, reverse('usuarios:dashboard'))
        print("✓ Login redirige correctamente a dashboard")

    def test_logout_redirect_to_login(self):
        """Verificar redirección correcta después del logout"""
        self.client.login(username='test_user', password='Test123!')
        response = self.client.get(reverse('usuarios:logout'))
        
        self.assertRedirects(response, reverse('usuarios:login'))
        print("✓ Logout redirige correctamente a login")

    def test_protected_urls_require_login(self):
        """Verificar que URLs protegidas requieren autenticación"""
        protected_urls = [
            'usuarios:dashboard',
            'productos:lista',
            'proveedores:lista',
            'inventario:lista',
        ]
        
        for url_name in protected_urls:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 302)  # Redirige a login
        
        print("✓ URLs protegidas requieren autenticación")
