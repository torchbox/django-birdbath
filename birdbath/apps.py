from django.apps import AppConfig


class BirdBathConfig(AppConfig):
    name = "birdbath"

    def ready(self):
        from . import system_checks

