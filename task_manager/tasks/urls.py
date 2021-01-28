from django.urls import path
from .views import (
    TaskIndexView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
)

app_name = 'tasks'

urlpatterns = [
    path('tasks/', TaskIndexView.as_view(), name='index'),
    path('tasks/create/', TaskCreateView.as_view(), name='create'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='delete'),
]
