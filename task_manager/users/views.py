from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserForm
from .mixins import UserLoginRequiredMixin, OwnerOnlyMixin


class UserIndexView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users/index.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('users:login')
    success_message = gettext_lazy("User has been registered")


class UserUpdateView(
    UserLoginRequiredMixin, OwnerOnlyMixin, SuccessMessageMixin, UpdateView
):
    model = User
    form_class = UserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:index')
    success_message = gettext_lazy("User has been updated")
    not_owner_message = gettext_lazy(
        "You don't have rights to update other user."
    )


class UserDeleteView(UserLoginRequiredMixin, OwnerOnlyMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:index')
    success_message = gettext_lazy("User has been deleted")
    not_owner_message = gettext_lazy(
        "You don't have rights to update other user."
    )

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_message = gettext_lazy("You've been logged in")


class UserLogoutView(LogoutView):
    info_message = gettext_lazy("You've been logged out")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, self.info_message)
        return super().dispatch(request, *args, **kwargs)
