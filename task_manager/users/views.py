from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import UserForm
from .mixins import UserLoginRequiredMixin, OwnerOnlyMixin


class UserIndexView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('users:login')
    success_message = _("User has been registered")


class UserUpdateView(
    UserLoginRequiredMixin, OwnerOnlyMixin, SuccessMessageMixin, UpdateView
):
    model = User
    form_class = UserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:index')
    success_message = _("User has been updated")


class UserDeleteView(UserLoginRequiredMixin, OwnerOnlyMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:index')
    template_name = 'users/delete.html'
    success_message = _("User has been deleted")

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_message = _("You've been logged in")


class UserLogoutView(LogoutView):
    info_message = _("You've been logged out")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, self.info_message)
        return super().dispatch(request, *args, **kwargs)
