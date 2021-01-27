from django.urls import path
from .views import (
    TaskIndexView,
)

app_name = 'tasks'

urlpatterns = [
    path('tasks/', TaskIndexView.as_view(), name='index'),
]
