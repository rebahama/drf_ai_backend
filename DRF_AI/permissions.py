from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow only the owner of the related request to edit or delete."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, "request"):
            return obj.request.user == request.user

        return getattr(obj, "user", None) == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Only admin users can edit or delete.
    Others can only read.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff
