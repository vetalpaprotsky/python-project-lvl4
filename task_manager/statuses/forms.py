from django.forms import ModelForm, CharField
from django.utils.translation import ugettext_lazy as _
from .models import Status


class StatusForm(ModelForm):
    name = CharField(label=_('Name'))

    class Meta:
        model = Status
        fields = ['name']
