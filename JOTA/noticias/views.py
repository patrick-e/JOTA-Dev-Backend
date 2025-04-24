from rest_framework import generics

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
    