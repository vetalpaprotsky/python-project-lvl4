from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
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
    success_message = _("Status has been created")


class StatusUpdateView(UserLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    context_object_name = 'status'
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _("Status has been updated")
