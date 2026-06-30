from rest_framework import permissions


class IsTaskAssignee(permissions.BasePermission):
    """Allow access only to the assigned user of a task."""

    def has_object_permission(self, request, view, obj):
        """Allow access only if the requesting user is the task's assignee."""
        
        return obj.assignee == request.user
   
    
class IsTaskBoardMember(permissions.BasePermission):
    """Allow access only to members of the task's board."""
    
    def has_object_permission(self, request, view, obj):
        """Allow access only if the requesting user is a member of the task's board."""

        return obj.board.members.filter(id=request.user.id).exists()
    

class IsCommentBoardMember(permissions.BasePermission):
    """Allow access only to members of the board the comment's task belongs to."""

    def has_permission(self, request, view):
        """Allows access only if the board exists and the user is a member."""

        task = view.get_task()   
        return task.board.members.filter(id=request.user.id).exists()

    def has_object_permission(self, request, view, obj):
        """Allow access only if the user is a member of the board the comment's task belongs to."""

        return obj.task.board.members.filter(id=request.user.id).exists()


class IsCommentAuthor(permissions.BasePermission):
    """Allow access only to the author of a comment."""

    def has_object_permission(self, request, view, obj):
        """Allow access only if the requesting user authored the comment."""

        return obj.author == request.user