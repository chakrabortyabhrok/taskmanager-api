from rest_framework.viewsets import ModelViewSet
from .models import Task
from .serializers import TaskSerializer
from .filters import TaskFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TaskViewSet(ModelViewSet):
    """ API ViewSet for managing tasks with filtering, searching, and pagination. """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer 
    lookup_field = 'pk'
    search_fields = ['title', 'description']

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    pagination_class = StandardPagination
    ordering_fields = ['due_date', 'created_at', 'title']
    
    def get_serializer(self, *args, **kwargs):
        
        if isinstance(kwargs.get('data'), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)
    