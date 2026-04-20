from django.apps import AppConfig


class TrocaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'troca'

    def ready(self) -> None:
        import troca.signals.handlers
