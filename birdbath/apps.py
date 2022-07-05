from django.apps import AppConfig


class BirdBathConfig(AppConfig):
    name = "birdbath"
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        from . import system_checks

