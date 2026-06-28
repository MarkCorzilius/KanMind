from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField(User, blank=True, related_name='member_boards')

    def __str__(self):
        return f"title: {self.title}, owner: {self.owner}, members: {self.members}"
