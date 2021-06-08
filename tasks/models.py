from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Task(models.Model):
    description = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk':self.pk})