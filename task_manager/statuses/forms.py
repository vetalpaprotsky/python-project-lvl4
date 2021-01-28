from django.forms import ModelForm
from django.utils.translation import gettext as _
from .models import Status


class StatusForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = _('Name')

    class Meta:
        model = Status
        fields = ['name']
