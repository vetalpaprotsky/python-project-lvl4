from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='authored_tasks'
    )
    assigned_user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='assigned_tasks', null=True
    )
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now)
