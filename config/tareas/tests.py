from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from .models import Tarea

class TareaModelTest(TestCase):
    def setUp(self):
        """Crea una tarea inicial para verificar reglas del modelo."""
        self.tarea = Tarea.objects.create(
            titulo="Preparar exposición de Django",
            descripcion="Revisar el archivo tests.py y hacer la demo",
            prioridad=Tarea.Prioridad.ALTA,
            completada=False
        )

    def test_creacion_y_valores_por_defecto(self):
        """Verifica que los datos del modelo se guarden correctamente y los defaults funcionen."""
        self.assertEqual(self.tarea.titulo, "Preparar exposición de Django")
        self.assertEqual(self.tarea.prioridad, "A")  # Guarda "A" en MySQL
        self.assertFalse(self.tarea.completada)      # default=False

    def test_representacion_str(self):
        """Verifica que el método __str__ devuelva el título."""
        self.assertEqual(str(self.tarea), "Preparar exposición de Django")

    def test_metodo_get_prioridad_display(self):
        """Verifica que get_prioridad_display() devuelva la etiqueta legible."""
        self.assertEqual(self.tarea.get_prioridad_display(), "Alta")


class TareaViewsSecurityTest(TestCase):
    def setUp(self):
        """Crea usuarios con diferentes niveles de acceso."""
        # 1. Usuario común (sin permisos especiales)
        self.user_comun = User.objects.create_user(
            username="estudiante", 
            password="password123"
        )
        
        # 2. Usuario Administrador con permisos de la app 'tareas'
        self.user_admin = User.objects.create_user(
            username="admin_tareas", 
            password="password123"
        )
        # Asigna permisos nativos
        perm_add = Permission.objects.get(codename="add_tarea")
        perm_change = Permission.objects.get(codename="change_tarea")
        perm_delete = Permission.objects.get(codename="delete_tarea")
        self.user_admin.user_permissions.add(perm_add, perm_change, perm_delete)

        # Tarea de prueba para editar/borrar
        self.tarea = Tarea.objects.create(
            titulo="Tarea de Prueba",
            prioridad=Tarea.Prioridad.MEDIA
        )

    def test_redireccion_usuario_no_autenticado(self):
        """LoginRequiredMixin: Redirige al login si no está logueado."""
        response = self.client.get(reverse('lista'))
        self.assertEqual(response.status_code, 302)  # Redirección HTTP
        self.assertIn('/login/', response.url)

    def test_acceso_vista_lista_usuario_logueado(self):
        """Usuario logueado puede acceder a la lista de tareas."""
        self.client.login(username="estudiante", password="password123")
        response = self.client.get(reverse('lista'))
        self.assertEqual(response.status_code, 200)  # OK
        self.assertTemplateUsed(response, 'tareas/tarea_list.html')

    def test_creacion_tarea_con_permiso(self):
        """PermissionRequiredMixin: Usuario con permiso puede crear una tarea vía POST."""
        self.client.login(username="admin_tareas", password="password123")
        
        response = self.client.post(reverse('crear'), {
            'titulo': 'Nueva Tarea desde Test',
            'descripcion': 'Probando el POST',
            'prioridad': Tarea.Prioridad.BAJA,
            'fecha_limite': '2026-12-31',
            'completada': False
        })
        
        # Verifica la redirección exitosa tras guardar (success_url = reverse_lazy('lista'))
        self.assertEqual(response.status_code, 302)
        # Verifica que el registro se creó físicamente en la BD temporal
        self.assertTrue(Tarea.objects.filter(titulo='Nueva Tarea desde Test').exists())

    def test_bloqueo_creacion_sin_permiso(self):
        """PermissionRequiredMixin: Devuelve 403 Forbidden a usuario sin permiso 'add_tarea'."""
        self.client.login(username="estudiante", password="password123")
        
        response = self.client.get(reverse('crear'))
        self.assertEqual(response.status_code, 403)  # Acceso Prohibido