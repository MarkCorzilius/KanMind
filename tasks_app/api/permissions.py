from rest_framework import permissions

class IsTaskAssignee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assignee == request.user
    
class IsTaskBoardMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.board.members.filter(id=request.user.id).exists()