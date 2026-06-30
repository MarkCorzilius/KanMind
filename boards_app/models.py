from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    """Represents a kanban board owned by a user with multiple members."""
    
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField(User, blank=True, related_name='member_boards')

    def __str__(self):
        """Return a readable string representation of the board."""
        
        return f"title: {self.title}, owner: {self.owner}, members: {self.members}"
