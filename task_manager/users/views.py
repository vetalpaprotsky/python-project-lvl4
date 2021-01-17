from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from .forms import UserRegisterFrom


def register(request):
    if request.method == 'POST':
        form = UserRegisterFrom(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User has been registered!')
            return redirect('users:login')
    else:
        form = UserRegisterFrom()
    return render(request, 'users/register.html', {'form': form})


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_message = "You've been logged in!"


class UserLogoutView(LogoutView):
    success_message = "You've been logged out!"

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
