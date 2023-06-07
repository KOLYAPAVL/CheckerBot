from django.apps import AppConfig
from django.core.signals import request_finished


class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'

    def ready(self):
        from . import signals
        request_finished.connect(signals.on_create_bot_message)
