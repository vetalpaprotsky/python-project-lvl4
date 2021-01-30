from django.views.generic import ListView, CreateView, UpdateView  # DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy
# from django.contrib import messages
from task_manager.users.mixins import UserLoginRequiredMixin
from .models import Label
from .forms import LabelForm


class LabelIndexView(UserLoginRequiredMixin, ListView):
    model = Label
    context_object_name = 'labels'
    template_name = 'labels/index.html'


class LabelCreateView(UserLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels:index')
    success_message = gettext_lazy("Label has been created")


class LabelUpdateView(UserLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    context_object_name = 'label'
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels:index')
    success_message = gettext_lazy("Label has been updated")
