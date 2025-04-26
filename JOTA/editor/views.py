from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthor, IsRegisteredAuthor

from .models import News
from .serializers import NewsSerializers

class NewsList(generics.ListCreateAPIView):
    serializer_class = NewsSerializers
    permission_classes = [IsAuthenticated, IsRegisteredAuthor]  # Adiciona a permissão personalizada

    def get_queryset(self):
        # Retorna apenas as notícias do autor autenticado
        return News.objects.filter(autor=self.request.user)

    def perform_create(self, serializer):
        # Associa a notícia ao autor autenticado
        serializer.save(autor=self.request.user)
        
class Newsdetail(generics.RetrieveDestroyAPIView):
    serializer_class = NewsSerializers
    queryset = News.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]

class Newsupdate(generics.RetrieveUpdateAPIView):
    serializer_class = NewsSerializers
    queryset = News.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
