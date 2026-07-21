from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import TaskViewSet, AskAIView, vectorstore_status, CreateSuperUserView#, DeleteAllTasksView, ClearVectorstoreView
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('tasks/ask_ai/', AskAIView.as_view(), name='ask-ai'),
    path('create-superuser/', CreateSuperUserView.as_view(), name='create-superuser'),
    path('vectorstore-status/', vectorstore_status, name='vectorstore-status'),
    #path('delete-all-tasks/', DeleteAllTasksView.as_view(), name='delete-all-tasks'),
    #path('clear-vectorstore/', ClearVectorstoreView.as_view(), name='clear-vectorstore'),
    #path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

] + router.urls
