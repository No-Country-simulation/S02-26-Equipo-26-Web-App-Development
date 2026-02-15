from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
# users/apps.py
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Gestión de Usuarios'
    
    def ready(self):
        """
        Este método se ejecuta cuando Django inicia.
        Aquí importamos los signals para que se registren.
        """
        import users.signals  # Importar signals
