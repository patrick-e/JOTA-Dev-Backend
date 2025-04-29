from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..serializers import UserDetailSerializer
from ..services import UserService
from rest_framework import permissions


class IsAdminOrSelf(permissions.BasePermission):
    """
    Permite acesso apenas se o usuário for admin ou o próprio usuário
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj == request.user


class UserManagementView(generics.GenericAPIView):
    """
    View para gerenciar usuários

    get:
    - Se usuário for admin: Lista todos os usuários
    - Se usuário comum: Retorna próprio perfil

    patch:
    - Se usuário for admin: Pode atualizar qualquer usuário
    - Se usuário comum: Pode atualizar apenas próprio perfil
    """
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelf]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            users = self.get_queryset()
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)

        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        try:
            updated_user = UserService.update_user_profile(request.user, request.data)
            serializer = self.get_serializer(updated_user)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
