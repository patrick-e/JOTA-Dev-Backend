from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define o módulo de configurações padrão do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JOTA.settings')

app = Celery('JOTA')

# Lê as configurações do Django e aplica ao Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre automaticamente tarefas em apps instalados
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
