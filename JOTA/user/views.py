from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
from django.contrib.auth.models import User

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
