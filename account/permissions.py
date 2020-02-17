from rest_framework import permissions


class UpdateOwnProfle(permissions.BasePermission):
    """allow user to edit there own permission """

    def has_object_permission(self, request, view, obj):
        """Check user is trying their own profile"""

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id

class SignUpPermission(permissions.BasePermission):
    """allow user to signup if they are noy login"""
    def has_object_permission(self, request, view, obj):
        """check if user loged in or not"""
        if request.user.is_authenticated:
            return False
        return True