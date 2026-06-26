from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import TaskViewSet, AskAIView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('tasks/ask_ai/', AskAIView.as_view(), name='ask-ai'),
] + router.urls
