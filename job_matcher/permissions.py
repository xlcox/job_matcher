from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrCreateOnly(BasePermission):
    """
    Позволяет выполнять POST всем аутентифицированным пользователям,
    а все остальные методы — только admin.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            # Разрешаем создавать резюме всем аутентифицированным (или даже анонимным, если нужно)
            return request.user.is_authenticated or request.user.is_anonymous
        else:
            # Для остальных методов — только admin
            return request.user.is_authenticated and request.user.is_admin
