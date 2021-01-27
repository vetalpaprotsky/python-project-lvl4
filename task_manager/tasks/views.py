from django.views.generic import ListView
from task_manager.users.mixins import UserLoginRequiredMixin
from .models import Task


class TaskIndexView(UserLoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
