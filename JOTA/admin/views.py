from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import News
from .serializers import NewsSerializers

class NewsList(generics.ListCreateAPIView):
    serializer_class = NewsSerializers

    def get_queryset(self):
        queryset = News.objects.all()
        return queryset
    
class Newsdetail(generics.RetrieveDestroyAPIView):
    serializer_class = NewsSerializers
    queryset = News.objects.all()
    
class Newsupdate(generics.RetrieveUpdateAPIView):
    serializer_class = NewsSerializers
    queryset = News.objects.all()
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    