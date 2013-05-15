from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet
        return obj.owner == request.user


class IsOwner(permissions.BasePermission):

    """
    Custom permisson to only allow owners
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsMember(permissions.BasePermission):

    """
    Custom permission to only allow who is
    the member of the circle
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.members
