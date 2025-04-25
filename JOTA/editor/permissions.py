from rest_framework.permissions import BasePermission

class IsAuthor(BasePermission):
    """
    Permissão que permite apenas ao autor da notícia acessá-la ou modificá-la.
    """

    def has_object_permission(self, request, view, obj):
        return obj.autor_auth.user == request.user