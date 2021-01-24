from django.db import models
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
