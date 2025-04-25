from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthor

from .models import News
from .serializers import NewsSerializers

class NewsList(generics.ListCreateAPIView):
    serializer_class = NewsSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna apenas as notícias do autor autenticado
        return News.objects.filter(autor_auth__user=self.request.user)

    def perform_create(self, serializer):
        # Associa a notícia ao autor autenticado
        autor_auth = self.request.user.autor_auth
        serializer.save(autor_auth=autor_auth)

class Newsdetail(generics.RetrieveDestroyAPIView):
    serializer_class = NewsSerializers
    queryset = News.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]

class Newsupdate(generics.RetrieveUpdateAPIView):
    serializer_class = NewsSerializers
    queryset = News.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
