"""Certificate management Django application configuration."""

from django.apps import AppConfig


class CertificatesConfig(AppConfig):
    """Django app configuration for the certificates application.

    Configures the certificates app and initializes signal handlers for
    automatic customer creation on user signup.

    Attributes:
        default_auto_field: Uses BigAutoField for model primary keys.
        name: Application name identifier ('certificates').
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'certificates'

    def ready(self) -> None:
        """Initialize the certificates app when Django starts.

        Imports and registers signal handlers for post-save operations
        like automatic customer creation.
        """
        import certificates.signals.handlers
