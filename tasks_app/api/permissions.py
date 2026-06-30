from rest_framework import permissions
from boards_app.models import Board
from tasks_app.models import Task
from rest_framework.exceptions import NotFound


class IsTaskAssignee(permissions.BasePermission):
    """Allow access only to the assigned user of a task."""
    def has_object_permission(self, request, view, obj):
        """Allow access only if the requesting user is the task's assignee."""
        return obj.assignee == request.user
   
    
class IsTaskBoardMember(permissions.BasePermission):
    """Allow access only to members of the task's board."""
    def has_permission(self, request, view):
        """Checks that the user is a member of the requested board and raises 404 if the board doesn’t exist."""
        board_id = request.data.get('board')
        if not board_id:
            return False
        if not Board.objects.filter(id=board_id).exists():
            raise NotFound('Board not found')
        return Board.objects.filter(id=board_id, members=request.user).exists()


    def has_object_permission(self, request, view, obj):
        """Allow access only if the requesting user is a member of the task's board."""
        return obj.board.members.filter(id=request.user.id).exists()
    

class IsCommentBoardMember(permissions.BasePermission):
    """Allow access only to members of the board the comment's task belongs to."""
    def has_permission(self, request, view):
        """Allows access only if the board exists and the user is a member."""
        task_pk = view.kwargs.get('task_pk')
        if not task_pk:
            return False
        if not Task.objects.filter(id=task_pk):
            raise NotFound('Task not found')
        return Task.objects.filter(id=task_pk, board__members=request.user).exists()

    def has_object_permission(self, request, view, obj):
        """Allow access only if the user is a member of the board the comment's task belongs to."""
        return obj.task.board.members.filter(id=request.user.id).exists()


class IsCommentAuthor(permissions.BasePermission):
    """Allow access only to the author of a comment."""
    def has_object_permission(self, request, view, obj):
        """Allow access only if the requesting user authored the comment."""
        return obj.author == request.user