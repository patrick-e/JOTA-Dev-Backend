from datetime import datetime
from pymongo import MongoClient
from django.dispatch import receiver
from .events import news_published, NewsPublishedEvent


class NewsAnalytics:
    def __init__(self):
        # Conecta ao MongoDB
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['jota_analytics']
        self.news_metrics = self.db['news_metrics']
        self.access_logs = self.db['access_logs']

    def log_news_access(self, news_id: int, user_id: int, access_type: str):
        """
        Registra acesso à notícia para análise
        """
        log = {
            'news_id': news_id,
            'user_id': user_id,
            'access_type': access_type,
            'timestamp': datetime.now(),
        }
        self.access_logs.insert_one(log)

    def update_news_metrics(self, news_id: int, metric_type: str):
        """
        Atualiza métricas da notícia
        """
        self.news_metrics.update_one(
            {'news_id': news_id},
            {
                '$inc': {f'metrics.{metric_type}': 1},
                '$set': {'last_updated': datetime.now()}
            },
            upsert=True
        )

    def get_news_metrics(self, news_id: int):
        """
        Retorna métricas da notícia
        """
        return self.news_metrics.find_one({'news_id': news_id})

    def get_popular_news(self, limit: int = 10):
        """
        Retorna as notícias mais acessadas
        """
        return self.news_metrics.find().sort('metrics.views', -1).limit(limit)


# Instância global do analytics
analytics = NewsAnalytics()


# Event handlers
@receiver(news_published)
def track_publication(sender, event: NewsPublishedEvent, **kwargs):
    """
    Registra métricas quando uma notícia é publicada
    """
    analytics.update_news_metrics(event.news_id, 'publications')


def track_news_view(news_id: int, user_id: int):
    """
    Registra visualização de notícia
    Deve ser chamado nas views quando uma notícia é acessada
    """
    analytics.log_news_access(news_id, user_id, 'view')
    analytics.update_news_metrics(news_id, 'views')


def get_news_views(news_ids: list):
    """
    Retorna as visualizações das notícias especificadas
    """
    metrics = []
    for news_id in news_ids:
        news_metric = analytics.get_news_metrics(news_id)
        if news_metric and 'metrics' in news_metric:
            metrics.append({
                'news_id': news_id,
                'total_views': news_metric['metrics'].get('views', 0),
                'last_updated': news_metric.get('last_updated')
            })
        else:
            metrics.append({
                'news_id': news_id,
                'total_views': 0,
                'last_updated': None
            })
    return metrics
