from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Create a custom authorazion for the user
       so that only authorized user can make crud
       operations on their created content
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
        