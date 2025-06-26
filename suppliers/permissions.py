from rest_framework import permissions


class IsActiveEmployee(permissions.BasePermission):
    """
    Доступ только у активных сотрудников (is_active=True)
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active
