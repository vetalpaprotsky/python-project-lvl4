from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Task


class TaskAuthorOnlyMixin:
    not_task_author_redirect_url = reverse_lazy('tasks:index')
    not_task_author_message = ''

    def dispatch(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        if task.author_id != request.user.id:
            if self.not_task_author_message:
                messages.error(request, self.not_task_author_message)
            return redirect(self.not_task_author_redirect_url)
        return super().dispatch(request, *args, **kwargs)
