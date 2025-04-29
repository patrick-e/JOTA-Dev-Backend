from django.urls import path
from .views.auth_views import RegisterView, LoginView, RefreshTokenView

app_name = 'user'

urlpatterns = [
    # Authentication endpoints
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
]
