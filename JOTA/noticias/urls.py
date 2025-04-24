from django.urls import path
from .views import NewsList, Newsdetail

urlpatterns = [
    path('news/', NewsList.as_view()),
    path('news/<int:pk>', Newsdetail.as_view())
] 
