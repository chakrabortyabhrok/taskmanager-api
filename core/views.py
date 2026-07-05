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
from rest_framework.decorators import api_view
from django.db import connection
from .ai_utils import ask_ai_about_tasks, add_task_to_vectorstore, get_vectorstore


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

        #Get answer from OpenAI
        answer = ask_ai_about_tasks(question)

        return Response({"answer": answer}, status=status.HTTP_200_OK)

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
    
@api_view(['GET'])
def chroma_status(request):
    vectorstore = get_vectorstore()
    count = vectorstore._collection.count()
    return Response({
        "tasks_in_chroma": count,
        "message": f"Currently {count} tasks are embedded in Chroma"
    })