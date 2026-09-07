from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Право для модераторов: просмотр и редактирование любых курсов и уроков, но без возможности создавать и удалять."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name="Модераторы").exists()


class IsOwner(BasePermission):
    """Право: пользователь является владельцем объекта"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrModerator(BasePermission):
    """Право: владелец или модератор"""

    def has_object_permission(self, request, view, obj):
        return (
            obj.owner == request.user
            or request.user.groups.filter(name="Модераторы").exists()
        )
