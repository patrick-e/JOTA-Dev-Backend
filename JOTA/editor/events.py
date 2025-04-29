from dataclasses import dataclass
from datetime import datetime
from django.dispatch import Signal, receiver
from django.db.models.signals import post_save
from .models import News


# Definição dos eventos
news_published = Signal()
news_updated = Signal()
news_scheduled = Signal()


@dataclass
class NewsEvent:
    """Classe base para eventos relacionados a notícias"""
    news_id: int
    timestamp: datetime
    actor_id: int


@dataclass
class NewsPublishedEvent(NewsEvent):
    """Evento emitido quando uma notícia é publicada"""
    previous_status: str


@dataclass
class NewsScheduledEvent(NewsEvent):
    """Evento emitido quando uma notícia é agendada"""
    scheduled_date: datetime


# Handlers dos eventos
@receiver(post_save, sender=News)
def handle_news_save(sender, instance, created, **kwargs):
    try:
        if not created and instance.status == 'published':
            event = NewsPublishedEvent(
                news_id=instance.id,
                timestamp=datetime.now(),
                actor_id=instance.autor.id,
                previous_status='draft'
            )
            news_published.send(sender=sender, event=event)

        if instance.data_de_publicacao > datetime.now().date():
            event = NewsScheduledEvent(
                news_id=instance.id,
                timestamp=datetime.now(),
                actor_id=instance.autor.id,
                scheduled_date=instance.data_de_publicacao
            )
            news_scheduled.send(sender=sender, event=event)
    except Exception as e:
        print(f"Erro ao processar evento post_save: {e}")


# Exemplo de consumer do evento de publicação
@receiver(news_published)
def notify_publication(sender, event, **kwargs):
    """
    Consumer que poderia disparar notificações quando uma notícia é publicada
    Em uma arquitetura mais robusta, isso seria um serviço separado
    """
    print(f"Notícia {event.news_id} foi publicada por {event.actor_id}")


# Exemplo de consumer do evento de agendamento
@receiver(news_scheduled)
def handle_scheduling(sender, event, **kwargs):
    """
    Consumer que poderia integrar com um serviço de calendário
    Em uma arquitetura mais robusta, isso seria um serviço separado
    """
    print(f"Notícia {event.news_id} agendada para {event.scheduled_date}")
