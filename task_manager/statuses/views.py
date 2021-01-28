from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _lazy
from django.contrib import messages
from task_manager.users.mixins import UserLoginRequiredMixin
from .models import Status
from .forms import StatusForm


class StatusIndexView(UserLoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class StatusCreateView(UserLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _lazy("Status has been created")


class StatusUpdateView(UserLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    context_object_name = 'status'
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _lazy("Status has been updated")


class StatusDeleteView(UserLoginRequiredMixin, DeleteView):
    model = Status
    context_object_name = 'status'
    success_url = reverse_lazy('statuses:index')
    template_name = 'statuses/delete.html'
    success_message = _lazy("Status has been deleted")

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)
