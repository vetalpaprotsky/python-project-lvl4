from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _lazy


class UserLoginRequiredMixin(LoginRequiredMixin):
    unauthorized_user_message = _lazy("You're not authorized! Please, log in.")

    def handle_no_permission(self):
        messages.error(self.request, self.unauthorized_user_message)
        return super().handle_no_permission()


class OwnerOnlyMixin:
    redirect_url_pattern = 'users:index'
    access_denied_message = _lazy("You don't have rights to update other user.")

    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != request.user.pk:
            messages.error(request, self.access_denied_message)
            return redirect(self.redirect_url_pattern)
        return super().dispatch(request, *args, **kwargs)
