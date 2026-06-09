from rest_framework.viewsets import ModelViewSet
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer  # Pass the CLASS, do not call it with ()
    lookup_field = 'id'  # Note: Your model didn't have a slug field, use 'id' or 'pk' unless you added one!

    def get_serializer(self, *args, **kwargs):
        # If the incoming data from Postman is a list [], automatically inject many=True
        if isinstance(kwargs.get('data'), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)