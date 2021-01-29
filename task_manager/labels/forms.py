from django.forms import ModelForm
from django.utils.translation import gettext as _
from .models import Label


class LabelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = _('Name')

    class Meta:
        model = Label
        fields = ['name']
