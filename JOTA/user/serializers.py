from django.contrib.auth.models import User
from rest_framework import serializers
from editor.models import AuthorProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        AuthorProfile.objects.create(user=user, nome_do_autor=user.username)
        return user