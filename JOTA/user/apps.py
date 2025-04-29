from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        """
        Importa os signals quando o app é carregado
        """
        import user.signals  # noqa: F401
