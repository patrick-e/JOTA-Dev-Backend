from django.contrib.auth.models import User
from rest_framework import serializers
from editor.models import AuthorProfile


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de usuário com dados básicos
    """
    first_name = serializers.CharField(required=True, write_only=True)
    role = serializers.ChoiceField(
        choices=AuthorProfile.ROLE_CHOICES,
        default="Leitor",
        write_only=True
    )
    is_pro = serializers.BooleanField(default=False, write_only=True)
    allowed_verticals = serializers.ListField(
        required=False,
        default=list,
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'first_name',
            'role',
            'is_pro',
            'allowed_verticals'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        # Remove os campos extras que não pertencem ao User
        role = validated_data.pop('role')
        is_pro = validated_data.pop('is_pro')
        allowed_verticals = validated_data.pop('allowed_verticals', [])

        # Cria o usuário
        user = User.objects.create_user(**validated_data)

        # Atualiza o perfil criado pelo signal
        author_profile = user.author_profile
        author_profile.role = role
        author_profile.save()

        # Atualiza o plano criado pelo signal
        client_plan = user.client_plan
        client_plan.is_pro = is_pro
        client_plan.allowed_verticals = allowed_verticals if is_pro else []
        client_plan.save()

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para retornar detalhes do usuário
    """
    role = serializers.CharField(source='author_profile.role')
    client_category = serializers.SerializerMethodField()
    allowed_verticals = serializers.ListField(source='client_plan.allowed_verticals')

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'client_category', 'allowed_verticals']

    def get_client_category(self, obj):
        return "PRO" if obj.client_plan.is_pro else "Comum"
