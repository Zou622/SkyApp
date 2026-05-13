from django.apps import AppConfig


class EmployesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employes'

    def ready(self):
        import employes.signals  # noqa: F401
