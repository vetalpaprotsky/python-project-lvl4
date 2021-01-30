from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect


# protected_url attribute is required.
class ProtectedDeleteMixin:
    success_message = ''
    protected_message = ''

    def delete(self, request, *args, **kwargs):
        try:
            result = super().delete(request, *args, **kwargs)
            if self.success_message:
                messages.success(request, self.success_message)
            return result
        except ProtectedError:
            if self.protected_message:
                messages.error(request, self.protected_message)
            return redirect(self.protected_url)
