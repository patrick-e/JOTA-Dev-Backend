from __future__ import absolute_import, unicode_literals

# Importa o Celery para que ele seja carregado com o Django
from .celery import app as celery_app

__all__ = ('celery_app',)

# Adicionando uma nova linha no final do arquivo