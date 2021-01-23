from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views.generic import ListView, View
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import UserForm
from .mixins import UserLoginRequiredMixin, OwnerOnlyMixin


class UserIndexView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(View):
    form_class = UserForm
    template_name = 'users/create.html'
    redirect_url_pattern = 'users:login'
    success_message = _("User has been registered")

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return redirect(self.redirect_url_pattern)
        return render(request, self.template_name, {'form': form})


class UserUpdateView(UserLoginRequiredMixin, OwnerOnlyMixin, View):
    form_class = UserForm
    template_name = 'users/update.html'
    redirect_url_pattern = 'users:index'
    success_message = _("User has been updated")

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return redirect(self.redirect_url_pattern)
        return render(request, self.template_name, {'form': form})


class UserDeleteView(UserLoginRequiredMixin, OwnerOnlyMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:index')
    template_name = 'users/delete.html'
    context_object_name = 'user'
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
