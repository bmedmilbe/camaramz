from django.apps import AppConfig


class TrocaConfig(AppConfig):
    """
    Application configuration for the 'Troca' module.

    This class handles the initialization of the application and ensures that
    decoupled logic, such as Signal Handlers, is correctly registered within
    the Django framework lifecycle.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'troca'

    def ready(self) -> None:
        """
        Lifecycle hook called by Django as soon as the application registry is fully populated.

        CRITICAL: We import the signals handler here to ensure that the @receiver decorators
        are executed and the signals are connected to their respective senders (e.g., User model).
        """
        # Import inside ready() to avoid 'AppRegistryNotReady' exceptions during startup
        import troca.signals.handlers
