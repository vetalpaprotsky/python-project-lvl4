from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_message = "You've been logged in!"


class UserLogoutView(LogoutView):
    success_message = "You've been logged out!"

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
