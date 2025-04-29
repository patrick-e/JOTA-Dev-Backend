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

# Cria o script de inicialização diretamente no Dockerfile
RUN echo '#!/bin/bash\n\
\n\
# Espera o banco de dados estar disponível\n\
echo "Aguardando o banco de dados..."\n\
sleep 5\n\
\n\
# Aplica as migrações\n\
echo "Aplicando migrações..."\n\
python JOTA/manage.py migrate --noinput\n\
\n\
# Coleta arquivos estáticos\n\
echo "Coletando arquivos estáticos..."\n\
python JOTA/manage.py collectstatic --noinput\n\
\n\
# Executa o comando fornecido\n\
exec "$@"' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

# Expõe a porta 8000
EXPOSE 8000

# Define o entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Define o comando padrão
CMD ["gunicorn", "JOTA.wsgi:application", "--bind", "0.0.0.0:8000"]