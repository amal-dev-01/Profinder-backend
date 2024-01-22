from rest_framework import permissions


class IsProfessionalAndNotBlocked(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.is_professional and not request.user.is_blocked
