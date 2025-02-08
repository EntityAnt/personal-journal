from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Проверяет, является ли пользователь автором."""

    message = "Вы не являетесь автором этой записи"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
