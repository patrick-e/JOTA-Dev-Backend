from django.urls import path
from .views import NewsList, Newsdetail,Newsupdate

urlpatterns = [
    path('news/', NewsList.as_view()),
    path('news/delete/<int:pk>', Newsdetail.as_view()),
    path('news/update/<int:pk>',Newsupdate.as_view())
] 
