from rest_framework import permissions

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    

class IsBoardMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.members.filter(id=request.user.id).exists()
    