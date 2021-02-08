from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
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


class LabelDeleteView(UserLoginRequiredMixin, DeleteView):
    model = Label
    context_object_name = 'label'
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels:index')
    protected_url = reverse_lazy('labels:index')
    success_message = gettext_lazy("Label has been deleted")
    protected_message = gettext_lazy("Can't delete label because it's in use")

    def delete(self, request, *args, **kwargs):
        label = get_object_or_404(Label, pk=kwargs['pk'])
        if label.task_set.exists():
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)
        result = super().delete(request, *args, **kwargs)
        messages.success(request, self.success_message)
        return result
