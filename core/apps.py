from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
    
#    def ready(self):
        # This runs when Django starts
#        from core.ai_utils import ensure_tasks_are_embedded
#        ensure_tasks_are_embedded()