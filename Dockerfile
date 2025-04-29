# Imagem base
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=JOTA.settings

# Instala dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements.txt primeiro para aproveitar o cache de camadas
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

# Cria diretório estático
RUN mkdir -p JOTA/static

# Expõe a porta 8000
EXPOSE 8000

# Script de inicialização
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Define o entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Define o comando padrão
CMD ["gunicorn", "JOTA.wsgi:application", "--bind", "0.0.0.0:8000"]