# boards_app/signals.py
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from boards_app.models import Board
from tasks_app.models import Task


@receiver(m2m_changed, sender=Board.members.through)
def unset_removed_members_from_tasks(sender, instance, action, pk_set, **kwargs):
    """Clear assignee/reviewer on tasks when a member is removed from a board."""
    if action == 'post_remove':
        Task.objects.filter(board=instance, assignee__in=pk_set).update(assignee=None)
        Task.objects.filter(board=instance, reviewer__in=pk_set).update(reviewer=None)