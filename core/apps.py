from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_feild = 'django.db.models.BigAutoFeild'
    name = 'core'

    def ready(self):
        import core.signals
    
#    def ready(self):
        # This runs when Django starts
#        from core.ai_utils import ensure_tasks_are_embedded
#        ensure_tasks_are_embedded()