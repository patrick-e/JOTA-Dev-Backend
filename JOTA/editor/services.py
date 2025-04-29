from django.db import models
from django.utils import timezone
from django.core.cache import cache
from django.core.paginator import Paginator
from rest_framework.exceptions import ValidationError
from .models import News
from .analytics import track_news_view


class NewsService:
    CACHE_TTL = 60 * 15  # 15 minutos
    PAGE_SIZE = 10

    @staticmethod
    def get_news_queryset(user, page=1):
        """
        Retorna o queryset de notícias paginado e com cache
        """
        cache_key = f"news_list_{user.id if user.is_authenticated else 'anonymous'}_page_{page}"
        cached_result = cache.get(cache_key)

        if cached_result:
            return cached_result

        # Define o queryset base
        if not user.is_authenticated:
            queryset = News.objects.filter(acesso="public", status="published")
        else:
            try:
                if hasattr(user, 'author_profile'):
                    if user.author_profile.role == "Admin":
                        queryset = News.objects.all()
                    elif user.author_profile.role == "Editor":
                        queryset = News.objects.filter(autor=user)
                    else:
                        # Usuário normal
                        if hasattr(user, 'client_plan') and user.client_plan.is_pro:
                            # Usuário PRO pode ver conteúdo público e PRO nas categorias permitidas
                            print("\nDEBUG - Usuário PRO:")
                            print(f"Verticais permitidas: {user.client_plan.allowed_verticals}")

                            queryset = News.objects.filter(
                                models.Q(acesso="public", status="published") |
                                models.Q(acesso="pro", status="published", categoria__in=user.client_plan.allowed_verticals)
                            )

                            print(f"Total de notícias encontradas: {queryset.count()}")
                            print("Query SQL:", queryset.query)
                            print("Notícias PRO encontradas:")
                            for news in queryset.filter(acesso="pro"):
                                print(f"- {news.titulo} (Categoria: {news.categoria}, Status: {news.status})")
                        else:
                            # Usuário comum só vê conteúdo público
                            queryset = News.objects.filter(acesso="public", status="published")
                else:
                    # Sem perfil de autor
                    if hasattr(user, 'client_plan') and user.client_plan.is_pro:
                        # Usuário PRO pode ver conteúdo público e PRO nas categorias permitidas
                        queryset = News.objects.filter(
                            models.Q(acesso="public", status="published") |
                            models.Q(acesso="pro", status="published", categoria__in=user.client_plan.allowed_verticals)
                        )
                    else:
                        # Usuário comum só vê conteúdo público
                        queryset = News.objects.filter(acesso="public", status="published")
            except AttributeError:
                # Fallback para erro de atributo
                queryset = News.objects.filter(acesso="public", status="published")

        queryset = queryset.order_by('-data_de_publicacao')  # Ordena por data de publicação
        paginator = Paginator(queryset, NewsService.PAGE_SIZE)
        result = paginator.get_page(page)

        # Armazena em cache
        cache.set(cache_key, {'queryset': queryset, 'page': result}, NewsService.CACHE_TTL)
        return {'queryset': queryset, 'page': result}

    @staticmethod
    def create_news(data, author):
        """
        Cria uma nova notícia com validação
        """
        required_fields = ['titulo', 'conteudo', 'categoria']
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Campo obrigatório: {field}")

        if len(data['titulo']) < 5:
            raise ValidationError("Título deve ter pelo menos 5 caracteres")

        if len(data['conteudo']) < 50:
            raise ValidationError("Conteúdo deve ter pelo menos 50 caracteres")

        news = News.objects.create(
            autor=author,
            **data
        )

        # Invalida cache relacionado
        cache.delete_pattern("news_list_*")
        return news

    @staticmethod
    def update_news(news_instance, data):
        """
        Atualiza uma notícia com validação
        """
        if 'titulo' in data and len(data['titulo']) < 5:
            raise ValidationError("Título deve ter pelo menos 5 caracteres")

        if 'conteudo' in data and len(data['conteudo']) < 50:
            raise ValidationError("Conteúdo deve ter pelo menos 50 caracteres")

        for attr, value in data.items():
            setattr(news_instance, attr, value)

        news_instance.save()

        # Invalida cache relacionado
        cache.delete_pattern("news_list_*")
        return news_instance

    @staticmethod
    def delete_news(news_id):
        """
        Remove uma notícia e limpa o cache
        """
        News.objects.filter(id=news_id).delete()
        cache.delete_pattern("news_list_*")

    @staticmethod
    def view_news(news_id, user_id):
        """
        Registra a visualização de uma notícia
        """
        track_news_view(news_id, user_id)
        cache_key = f"news_views_{news_id}"
        cache.delete(cache_key)

    @staticmethod
    def publish_scheduled_news():
        """
        Publica notícias agendadas para a data atual
        """
        today = timezone.now().date()
        published = News.objects.filter(
            data_de_publicacao=today,
            status="draft"
        ).update(status="published")

        if published > 0:
            cache.delete_pattern("news_list_*")
        return published
