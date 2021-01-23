from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views import generic
from django.contrib.auth.models import User
from .forms import UserForm
from .mixins import UserLoginRequiredMixin, OwnerOnlyMixin


class IndexView(generic.ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class CreateView(generic.View):
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


class UpdateView(UserLoginRequiredMixin, OwnerOnlyMixin, generic.View):
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


def delete(request):
    pass


class LoginView(SuccessMessageMixin, auth_views.LoginView):
    template_name = 'users/login.html'
    success_message = _("You've been logged in")


class LogoutView(auth_views.LogoutView):
    info_message = _("You've been logged out")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, self.info_message)
        return super().dispatch(request, *args, **kwargs)
