from django.forms import ModelForm
from django.utils.translation import gettext as _
from .models import Task


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = _('Name')
        self.fields['description'].label = _('Description')
        self.fields['status'].label = _('Status')
        self.fields['executor'].label = _('Executor')
        self.fields['labels'].label = _('Labels')

    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'executor',
            'labels',
        ]
