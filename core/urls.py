from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import TaskViewSet, AskAIView, chroma_status

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('tasks/ask_ai/', AskAIView.as_view(), name='ask-ai'),
    path('chroma-status/', chroma_status, name='chroma-status'),#After adding this, I can check anytime by visiting: https://taskmanager-api-d57o.onrender.com/api/chroma-status/
] + router.urls
