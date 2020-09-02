from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.


class MyDev(AbstractUser):
    pass


class Bug(models.Model):
    title = models.CharField(max_length=50)

    time_date = models.DateTimeField(default=timezone.now)

    description = models.TextField()

    assigned_by_dev = models.ForeignKey(
        MyDev, on_delete=models.CASCADE, related_name="assigned_to_dev")

    assigned_to_dev = models.ForeignKey(
        MyDev, on_delete=models.CASCADE, related_name="assigned_by_dev", blank=True, null=True)

    completed_by_dev = models.ForeignKey(
        MyDev, on_delete=models.CASCADE, related_name="completed_by_dev", blank=True, null=True)

    NEW = 'NE'
    IN_PROGRESS = 'IP'
    DONE = 'DO'
    INVALID = 'IN'
    COMPLETION_STATUS_CHOICE = [
        (NEW, 'New'),
        (IN_PROGRESS, 'In Progress'),
        (DONE, 'Done'),
        (INVALID, 'Invalid')
    ]
    completion_status_choice = models.CharField(
        max_length=2, choices=COMPLETION_STATUS_CHOICE, default=NEW)

    def __str__(self):
        return self.title
