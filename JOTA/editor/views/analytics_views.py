from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Avg, Q
from django.utils import timezone
from django.core.cache import cache
from datetime import timedelta
from ..models import News
from ..analytics import get_news_views
from user.permissions import IsAdmin, IsEditor


class NewsAnalytics(APIView):
    """
    Análise de métricas de notícias.

    get:
    Retorna estatísticas detalhadas sobre as notícias:
    - Resumo geral (total, publicadas, rascunhos)
    - Tendências de publicação (semanal, mensal)
    - Distribuição por categoria
    - Distribuição por tipo de acesso
    - Top 5 notícias por visualizações
    - Métricas de tempo médio de publicação

    Para editores, mostra apenas suas próprias notícias.
    Para admins, mostra todas as notícias.
    Resultados são cacheados por 5 minutos.
    """
    permission_classes = [IsAdmin | IsEditor]
    CACHE_TTL = 60 * 5  # 5 minutos

    def get(self, request):
        user = request.user
        cache_key = f"news_analytics_{user.id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        # Base queryset
        queryset = News.objects.all()
        if not IsAdmin().has_permission(request, self):
            queryset = queryset.filter(autor=user)

        # Período de análise
        now = timezone.now()
        last_week = now - timedelta(days=7)
        last_month = now - timedelta(days=30)

        # Estatísticas básicas
        total_news = queryset.count()
        published_news = queryset.filter(status="published").count()
        draft_news = queryset.filter(status="draft").count()

        # Tendências de publicação
        weekly_publications = queryset.filter(data_de_publicacao__gte=last_week).count()
        monthly_publications = queryset.filter(data_de_publicacao__gte=last_month).count()

        # Distribuição por categoria
        categories = queryset.values('categoria').annotate(
            total=Count('id'),
            published=Count('id', filter=Q(status="published")),
            draft=Count('id', filter=Q(status="draft"))
        ).order_by('-total')

        # Distribuição por tipo de acesso
        access_distribution = queryset.values('acesso').annotate(
            total=Count('id')
        ).order_by('-total')

        # Métricas de tempo
        avg_draft_time = queryset.filter(status="published").aggregate(
            avg_time=Avg('data_de_publicacao')
        )['avg_time']

        # Visualizações
        news_ids = queryset.values_list('id', flat=True)
        views_data = get_news_views(list(news_ids))

        # Top notícias por visualizações
        top_news = []
        if views_data:
            news_views = {view['news_id']: view['total_views'] for view in views_data}
            top_news = queryset.filter(id__in=news_views.keys()).values('id', 'titulo').annotate(
                views=Count('id')
            )
            for news in top_news:
                news['views'] = news_views.get(news['id'], 0)
            top_news = sorted(top_news, key=lambda x: x['views'], reverse=True)[:5]

        data = {
            'summary': {
                'total_news': total_news,
                'published_news': published_news,
                'draft_news': draft_news,
                'weekly_publications': weekly_publications,
                'monthly_publications': monthly_publications,
                'avg_draft_time_days': avg_draft_time.days if avg_draft_time else 0
            },
            'categories_distribution': list(categories),
            'access_distribution': list(access_distribution),
            'top_news': list(top_news),
            'views_data': views_data
        }

        # Armazena em cache
        cache.set(cache_key, data, self.CACHE_TTL)
        return Response(data)


class AuthorAnalytics(APIView):
    """
    Análise de métricas por autor (apenas para admins).

    get:
    Retorna estatísticas detalhadas por autor:
    - Total de notícias
    - Notícias publicadas e rascunhos
    - Publicações mensais
    - Distribuição por tipo de acesso (público/pro)
    - Métricas de produtividade
    - Tempo médio até publicação

    Resultados são cacheados por 15 minutos.
    Requer permissões de administrador.
    """
    permission_classes = [IsAdmin]
    CACHE_TTL = 60 * 15  # 15 minutos

    def get(self, request):
        cache_key = "author_analytics"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        # Período de análise
        now = timezone.now()
        last_month = now - timedelta(days=30)

        # Estatísticas por autor
        author_stats = News.objects.values(
            'autor__username',
            'autor__email'
        ).annotate(
            total_news=Count('id'),
            published_news=Count('id', filter=Q(status="published")),
            draft_news=Count('id', filter=Q(status="draft")),
            monthly_publications=Count(
                'id',
                filter=Q(data_de_publicacao__gte=last_month, status="published")
            ),
            public_news=Count('id', filter=Q(acesso="public")),
            pro_news=Count('id', filter=Q(acesso="pro"))
        ).order_by('-total_news')

        # Produtividade média
        productivity = News.objects.values(
            'autor__username'
        ).filter(
            data_de_publicacao__gte=last_month
        ).annotate(
            avg_time_to_publish=Avg('data_de_publicacao')
        )

        data = {
            'author_statistics': list(author_stats),
            'productivity_metrics': list(productivity)
        }

        # Armazena em cache
        cache.set(cache_key, data, self.CACHE_TTL)
        return Response(data)
