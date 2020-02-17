from rest_framework import permissions


class UpdateOwnProfle(permissions.BasePermission):
    """allow user to edit there own permission """

    def has_object_permission(self, request, view, obj):
        """Check user is trying their own profile"""

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
