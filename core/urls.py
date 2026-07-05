from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import TaskViewSet, AskAIView, BackfillChromaView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('tasks/ask_ai/', AskAIView.as_view(), name='ask-ai'),
    path('tasks/backfill-chroma/', BackfillChromaView.as_view(), name='backfill-chroma'),
] + router.urls
