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
from .ai_utils import ask_ai_about_tasks, backfill_tasks_to_chroma, add_task_to_vectorstore


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
    
class BackfillChromaView(APIView):
    """
    Temporary endpoint to backfill tasks into Chroma.
    Remove this after one-time use.
    """
    def post(self, request):
        secret_key = request.data.get("secret_key", "")

        if secret_key != "backfill-chroma-2026":
            return Response(
                {"error": "Invalid secret key"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            tasks = Task.objects.all()
            success_count = 0
            failed_count = 0

            for task in tasks:
                try:
                    add_task_to_vectorstore(task)
                    success_count += 1
                except Exception as e:
                    failed_count += 1
                    print(f"Failed to embed task {task.id}: {e}")

            return Response({
                "message": "Backfill completed",
                "total_tasks": tasks.count(),
                "successfully_added": success_count,
                "failed": failed_count
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )