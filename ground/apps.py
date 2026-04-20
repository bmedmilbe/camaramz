from django.apps import AppConfig


class GroundConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ground'

    def ready(self) -> None:
        import ground.signals.handlers
