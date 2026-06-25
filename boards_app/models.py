from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Board(models.Model):
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField(User, blank=True, related_name='member_boards')


class Comments(models.Model):
    pass


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = 'to-do', 'To Do'
        IN_PROGRESS = 'in-progress', 'In Progress'
        REVIEW = 'in-review', 'In Review'
        DONE = 'done', 'Done'

    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    priority = models.CharField( max_length=20, choices=Priority.choices, default=Priority.LOW)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_tasks')
    due_date = models.DateField(null=True, blank=True)
    