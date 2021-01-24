from django.views.generic import ListView, CreateView
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
