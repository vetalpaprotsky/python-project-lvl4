from django.urls import path
from .views import (
    TaskIndexView,
    TaskCreateView,
)

app_name = 'tasks'

urlpatterns = [
    path('tasks/', TaskIndexView.as_view(), name='index'),
    path('tasks/create/', TaskCreateView.as_view(), name='create'),
]
