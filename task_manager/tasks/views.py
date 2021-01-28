from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy
from django.contrib import messages
from task_manager.users.mixins import UserLoginRequiredMixin
from .models import Task
from .forms import TaskForm
from .mixins import TaskAuthorOnlyMixin


class TaskIndexView(UserLoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'


class TaskCreateView(UserLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:index')
    success_message = gettext_lazy("Task has been created")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(UserLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    context_object_name = 'task'
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:index')
    success_message = gettext_lazy("Task has been updated")


class TaskDeleteView(UserLoginRequiredMixin, TaskAuthorOnlyMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:index')
    success_message = gettext_lazy("Task has been deleted")
    not_task_author_message = gettext_lazy("Task can be deleted only by author")

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)
