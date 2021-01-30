from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy
from task_manager.users.mixins import UserLoginRequiredMixin
from task_manager.mixins import ProtectedDeleteMixin
from .models import Status
from .forms import StatusForm


class StatusIndexView(UserLoginRequiredMixin, ListView):
    model = Status
    context_object_name = 'statuses'
    template_name = 'statuses/index.html'


class StatusCreateView(UserLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:index')
    success_message = gettext_lazy("Status has been created")


class StatusUpdateView(UserLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    context_object_name = 'status'
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:index')
    success_message = gettext_lazy("Status has been updated")


class StatusDeleteView(
    UserLoginRequiredMixin, ProtectedDeleteMixin, DeleteView
):
    model = Status
    context_object_name = 'status'
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:index')
    protected_url = reverse_lazy('statuses:index')
    success_message = gettext_lazy("Status has been deleted")
    protected_message = gettext_lazy("Can't delete status because it's in use")
