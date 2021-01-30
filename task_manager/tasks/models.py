from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='authored_tasks'
    )
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='tasks', null=True, blank=True
    )
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now)
    labels = models.ManyToManyField(Label, blank=True)

    def __str__(self):
        return self.name
