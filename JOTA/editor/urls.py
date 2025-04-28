from django.urls import path
from .views.news_views import NewsList, NewsDetail, NewsUpdate
from .views.analytics_views import NewsAnalytics, AuthorAnalytics

app_name = 'editor'

urlpatterns = [
    # Endpoints de notícias
    path('news/', NewsList.as_view(), name='news-list'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news-detail'),
    path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news-update'),

    # Endpoints de análise
    path('analytics/news/', NewsAnalytics.as_view(), name='news-analytics'),
    path('analytics/authors/', AuthorAnalytics.as_view(), name='author-analytics'),
]
