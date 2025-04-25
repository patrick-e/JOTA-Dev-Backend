from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import NewsList, Newsdetail, Newsupdate

urlpatterns = [
    path('news/', NewsList.as_view()),
    path('news/delete/<int:pk>', Newsdetail.as_view()),
    path('news/update/<int:pk>', Newsupdate.as_view()),
    path('author/login/', TokenObtainPairView.as_view(), name='author_login'),
    path('author/token/refresh/', TokenRefreshView.as_view(), name='author_token_refresh'),
]
