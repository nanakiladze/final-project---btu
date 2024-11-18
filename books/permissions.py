
from rest_framework import permissions


class IsStaffUser(permissions.BasePermission):
    """
    Custom permission to allow access only to staff users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsAuthorOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object or staff members to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the object or staff.
        return obj.user == request.user or request.user.is_staff
