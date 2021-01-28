from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy
from django.urls import reverse_lazy


class UserLoginRequiredMixin(LoginRequiredMixin):
    unauthorized_user_message = gettext_lazy(
        "You're not authorized! Please, log in."
    )

    def handle_no_permission(self):
        messages.error(self.request, self.unauthorized_user_message)
        return super().handle_no_permission()


class OwnerOnlyMixin:
    not_owner_redirect_url = reverse_lazy('users:index')
    not_owner_message = ''

    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != request.user.pk:
            if self.not_owner_message:
                messages.error(request, self.not_owner_message)
            return redirect(self.not_owner_redirect_url)
        return super().dispatch(request, *args, **kwargs)
