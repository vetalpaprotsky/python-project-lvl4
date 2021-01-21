from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserForm


class IndexView(generic.ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


def create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("User has been registered"))
            return redirect('users:login')
    else:
        form = UserForm()
    return render(request, 'users/create.html', {'form': form})


@login_required
def update(request, pk):
    user = request.user

    # TODO: This should be moved to some decorator.
    if pk != user.pk:
        messages.error(request, _("You don't have rights to update other user"))
        return redirect('users:index')

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _("User has been updated"))
            return redirect('users:index')
    else:
        form = UserForm(instance=user)

    return render(request, 'users/update.html', {'form': form})


class LoginView(SuccessMessageMixin, auth_views.LoginView):
    template_name = 'users/login.html'
    success_message = _("You've been logged in")


class LogoutView(auth_views.LogoutView):
    info_message = _("You've been logged out")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, self.info_message)
        return super().dispatch(request, *args, **kwargs)
