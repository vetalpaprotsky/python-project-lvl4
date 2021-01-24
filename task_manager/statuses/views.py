from django.views.generic import ListView
from task_manager.users.mixins import UserLoginRequiredMixin
from .models import Status


class StatusIndexView(UserLoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'
