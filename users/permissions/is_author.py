from rest_framework import permissions


class IsNotAuthor(permissions.BasePermission):
    """
    Custom permission to only allow non-authors of a course to be members.
    """

    def has_object_permission(self, request, view, obj):
        # obj here would be a course instance
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check if the user is the author of the course
        return obj.author != request.user
