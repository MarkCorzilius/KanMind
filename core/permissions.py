from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Allow access only to the owner of an object."""

    def has_object_permission(self, request, view, obj):
        """Allow access only if the requesting user is the object owner."""
        return obj.owner == request.user
    

class IsBoardMember(permissions.BasePermission):
    """Allow access only to members of the related board."""

    def has_object_permission(self, request, view, obj):
        """Allow access only if the requesting user is a member of the board."""
        return obj.members.filter(id=request.user.id).exists()