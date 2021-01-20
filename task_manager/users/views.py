from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views import generic
from django.contrib.auth.models import User
from .forms import UserRegisterFrom


class IndexView(generic.ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


def create(request):
    if request.method == 'POST':
        form = UserRegisterFrom(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("User has been registered"))
            return redirect('users:login')
    else:
        form = UserRegisterFrom()
    return render(request, 'users/create.html', {'form': form})


class LoginView(SuccessMessageMixin, auth_views.LoginView):
    template_name = 'users/login.html'
    success_message = _("You've been logged in")


class LogoutView(auth_views.LogoutView):
    info_message = _("You've been logged out")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, self.info_message)
        return super().dispatch(request, *args, **kwargs)
