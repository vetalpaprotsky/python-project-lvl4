from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class UserLoginRequiredMixin:
    login_url_pattern = settings.LOGIN_URL
    unauthorized_user_message = _("You're not authorized! Please, log in.")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.unauthorized_user_message)
            return redirect(self.login_url_pattern)
        return super().dispatch(request, *args, **kwargs)


class OwnerOnlyMixin:
    redirect_url_pattern = 'users:index'
    access_denied_message = _("You don't have rights to update other user.")

    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != request.user.pk:
            messages.error(request, self.access_denied_message)
            return redirect(self.redirect_url_pattern)
        return super().dispatch(request, *args, **kwargs)
