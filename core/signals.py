from django.db.models.signals import post_save
from  django.dispatch import receiver
from .models import Task
from .ai_utils import add_task_to_vectorstore

@receiver(post_save, sender=Task)
def embeded_task_after_save(sender, instance, **kwargs):
    try:
        add_task_to_vectorstore(instance)
    except Exception as e:
        print(f"Chroma embedding failed for task {instance.id}: {e}")
