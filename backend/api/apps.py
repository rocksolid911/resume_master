"""
API Application Configuration
"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    verbose_name = 'Resume Builder API'

    def ready(self):
        """Import signals when app is ready"""
        import api.signals
