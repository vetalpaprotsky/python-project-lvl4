from django.forms import ModelForm
from .models import Status


# TODO: Translate form field.
class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ['name']
