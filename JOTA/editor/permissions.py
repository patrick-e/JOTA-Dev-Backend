from rest_framework.permissions import BasePermission

class IsAuthor(BasePermission):
    """
    Permissão que permite apenas ao autor da notícia acessá-la ou modificá-la.
    """

    def has_object_permission(self, request, view, obj):
        return obj.autor_auth.user == request.user

class IsRegisteredAuthor(BasePermission):
    """
    Permissão que permite apenas autores registrados pelo administrador criar notícias.
    """

    def has_permission(self, request, view):
        # Verifica se o usuário está autenticado e possui um perfil de autor
        return request.user.is_authenticated and hasattr(request.user, 'author_profile')