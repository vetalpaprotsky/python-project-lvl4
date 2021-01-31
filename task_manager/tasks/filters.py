from django_filters import FilterSet, ChoiceFilter, BooleanFilter
from django.forms import CheckboxInput
from django.utils.translation import gettext, gettext_lazy
from task_manager.labels.models import Label
from .models import Task


class TasksFilter(FilterSet):
    label = ChoiceFilter(
        method='filter_by_label',
        label=gettext_lazy('Label'),
    )

    self_tasks = BooleanFilter(
        method='filter_by_author',
        label=gettext_lazy('Only my tasks'),
        widget=CheckboxInput,
    )

    def filter_by_author(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    def filter_by_label(self, queryset, name, value):
        if value:
            return queryset.filter(labels__id=value)
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['status'].label = gettext('Status')
        self.filters['executor'].label = gettext('Executor')
        # Load "label" choices in __init__ method.
        # That way they will be loaded lazily.
        self.filters['label'].extra['choices'] = (
            (label.id, label.name) for label in Label.objects.all()
        )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']
