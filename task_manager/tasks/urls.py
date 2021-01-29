from django.urls import path
from .views import (
    TaskIndexView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
)

app_name = 'tasks'

urlpatterns = [
    path('tasks/', TaskIndexView.as_view(), name='index'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='detail'),
    path('tasks/create/', TaskCreateView.as_view(), name='create'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='delete'),
]
