from rest_framework.viewsets import ModelViewSet
from .models import Task
from .serializers import TaskSerializer
from .filters import TaskFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from .ai_utils import ask_ai_about_tasks


class AskAIView(APIView):
    """
    API endpoint to ask questions about tasks using natural language.
    """

    def post(self, request):
        question = request.data.get('question', '').strip()

        if not question:
            return Response(
                {"error": "Question is required."},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        #Fetch all tasks
        tasks = Task.objects.all()

        if not tasks.exists():
            return Response(
                {"answer": "You don't have any tasks yet."},
                status=status.HTTP_200_OK
            )
        #Get answer from OpenAI
        answer = ask_ai_about_tasks(question, tasks)

        return Response({"answers": answer}, status=status.HTTP_200_OK)

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
    