from django.apps import AppConfig


class EmployesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employes'
<<<<<<< HEAD

    def ready(self):
        import employes.signals  # noqa: F401
=======
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
