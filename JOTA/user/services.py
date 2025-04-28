from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework_simplejwt.tokens import RefreshToken
from editor.models import AuthorProfile
from .models import ClientPlan
import re

class AuthService:
    @staticmethod
    def validate_password(password):
        """
        Valida a senha do usuário
        - Mínimo 8 caracteres
        - Pelo menos uma letra maiúscula
        - Pelo menos uma letra minúscula
        - Pelo menos um número
        """
        if len(password) < 8:
            raise ValidationError("A senha deve ter pelo menos 8 caracteres")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("A senha deve conter pelo menos uma letra maiúscula")
        if not re.search(r"[a-z]", password):
            raise ValidationError("A senha deve conter pelo menos uma letra minúscula")
        if not re.search(r"\d", password):
            raise ValidationError("A senha deve conter pelo menos um número")

    @staticmethod
    def validate_username(username):
        """
        Valida o nome de usuário
        - Entre 3 e 30 caracteres
        - Apenas letras, números e underscores
        """
        if not re.match(r"^[a-zA-Z0-9_]{3,30}$", username):
            raise ValidationError(
                "Nome de usuário deve ter entre 3 e 30 caracteres e conter apenas letras, números e underscore"
            )

    @staticmethod
    def create_user(data):
        """
        Cria um novo usuário com validações
        """
        # Validações
        AuthService.validate_username(data['username'])
        AuthService.validate_password(data['password'])
        validate_email(data['email'])

        # Verifica se usuário já existe
        if User.objects.filter(username=data['username']).exists():
            raise ValidationError("Nome de usuário já está em uso")
        if User.objects.filter(email=data['email']).exists():
            raise ValidationError("Email já está em uso")

        # Cria o usuário
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )

        tokens = None
        try:
            # Verifica se é um autor autorizado
            author_profile = AuthorProfile.objects.get(user=user)
            if author_profile.role in ["Admin", "Editor"]:
                tokens = AuthService.generate_tokens(user)
        except AuthorProfile.DoesNotExist:
            # Cria um plano básico para o usuário
            ClientPlan.objects.create(
                user=user,
                is_pro=False,
                allowed_verticals=[]
            )

        return user, tokens

    @staticmethod
    def generate_tokens(user):
        """
        Gera tokens JWT para um usuário
        """
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

class UserService:
    @staticmethod
    def get_user_permissions(user):
        """
        Retorna as permissões do usuário baseadas em seu perfil
        """
        permissions = {
            'is_admin': False,
            'is_editor': False,
            'is_pro': False,
            'allowed_verticals': [],
            'can_create_news': False,
            'can_edit_news': False,
            'can_delete_news': False,
            'can_view_analytics': False
        }

        if not user.is_authenticated:
            return permissions

        try:
            if hasattr(user, 'author_profile'):
                role = user.author_profile.role
                permissions.update({
                    'is_admin': role == "Admin",
                    'is_editor': role == "Editor",
                    'can_create_news': role in ["Admin", "Editor"],
                    'can_edit_news': role in ["Admin", "Editor"],
                    'can_delete_news': role in ["Admin", "Editor"],
                    'can_view_analytics': role in ["Admin", "Editor"]
                })

            if hasattr(user, 'client_plan'):
                permissions.update({
                    'is_pro': user.client_plan.is_pro,
                    'allowed_verticals': user.client_plan.allowed_verticals
                })

        except (AuthorProfile.DoesNotExist, ClientPlan.DoesNotExist):
            pass

        return permissions

    @staticmethod
    def update_user_profile(user, data):
        """
        Atualiza o perfil do usuário
        """
        if 'email' in data:
            validate_email(data['email'])
            if User.objects.exclude(id=user.id).filter(email=data['email']).exists():
                raise ValidationError("Email já está em uso")
            user.email = data['email']

        if 'password' in data:
            AuthService.validate_password(data['password'])
            user.set_password(data['password'])

        user.save()
        return user