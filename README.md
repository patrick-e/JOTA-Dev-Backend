# JOTA Backend Challenge

Este repositório contém a base inicial para o desenvolvimento do Case Backend - JOTA, proposto como parte de um processo seletivo. O objetivo é construir uma API RESTful utilizando Django, focando em escalabilidade, segurança e boas práticas de desenvolvimento.

## Objetivo do Projeto

Desenvolver uma API para a gestão de notícias, com suporte a diferentes perfis de usuários, autenticação JWT, agendamento de publicações e controle de acesso com base em planos contratados (JOTA Info e JOTA PRO). O sistema deve ser eficiente e escalável, utilizando processamento assíncrono para tarefas de longa duração.

## Tecnologias Utilizadas

- **Linguagem**: Python 3.12+
- **Framework**: Django 5.2 + Django REST Framework
- **Banco de Dados**: PostgreSQL
- **Autenticação**: JWT (com djangorestframework-simplejwt)
- **Processamento Assíncrono**: Celery + Redis (planejado)
- **Documentação da API**: Swagger (drf-yasg) (planejado)
- **Containerização**: Docker + Docker Compose
- **Testes**: Pytest + coverage
- **Outras Dependências**: Pillow para manipulação de imagens

## Estrutura do Projeto

```bash
JOTA/
├── manage.py
├── JOTA/                      # Configurações globais do projeto
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── editor/                  # App responsável por CRUD de notícias 
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── requirements.txt           # Dependências do projeto
├── docker-compose.yml         # Configuração do Docker Compose
├── .env                       # Variáveis de ambiente (não versionado)
├── .env.exemple               # Exemplo de variáveis de ambiente
└── README.md                  # Documentação do projeto
```

## Configuração do Ambiente

### Pré-requisitos

- Python 3.12+
- Docker e Docker Compose
- PostgreSQL (para desenvolvimento local)

### Configuração Inicial

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/JOTA-Dev-Backend.git
   cd JOTA-Dev-Backend
   ```

2. **Configure o ambiente virtual**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .\.venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**:
   ```bash
   cp .env.exemple .env
   ```
   - Edite o arquivo `.env` para personalizar as configurações:
     ```
     POSTGRES_PASSWORD=sua_senha
     POSTGRES_USER=seu_usuario
     POSTGRES_DB=seu_banco
     ```

### Usando Docker

1. **Inicie os serviços com Docker Compose**:
   ```bash
   docker-compose up -d
   ```

2. **Acesse o Adminer**:
   - Abra o navegador e acesse `http://localhost:8080`
   - Dados de conexão:
     - Sistema: PostgreSQL
     - Servidor: db
     - Usuário: definido em `.env`
     - Senha: definida em `.env`
     - Base de dados: definida em `.env`

### Configuração do Django

1. **Execute as migrações**:
   ```bash
   python JOTA/manage.py migrate
   ```

2. **Crie um superusuário** (opcional):
   ```bash
   python JOTA/manage.py createsuperuser
   ```

3. **Inicie o servidor de desenvolvimento**:
   ```bash
   python JOTA/manage.py runserver
   ```

4. **Acesse a aplicação**:
   - Interface administrativa: `http://localhost:8000/admin/`
   - API: `http://localhost:8000/api/`

## Endpoints da API

### Notícias

- **Listar e Criar Notícias**:
  - **GET** `/api/news/`
  - **POST** `/api/news/`
  - Campos esperados no POST:
    ```json
    {
      "titulo": "string",
      "subtitulo": "string",
      "conteudo": "string",
      "data_de_publicacao": "YYYY-MM-DD",
      "autor": "string",
      "status": "draft|published",
      "categoria": "poder|tributos|saude|energia|trabalhista",
      "acesso": "public|pro",
      "imagem": "file"
    }
    ```

- **Detalhar e Excluir Notícia**:
  - **GET** `/api/news/<id>/`
  - **DELETE** `/api/news/<id>/`

## Testes

Para executar os testes, utilize o comando:
```bash
python JOTA/manage.py test
```

## Próximos Passos

- ✅ Configuração inicial do ambiente com Django + PostgreSQL.
- ✅ Implementação do CRUD de notícias.
- 🔲 Adicionar autenticação JWT.
- 🔲 Implementar controle de acesso baseado em planos.
- 🔲 Configurar Swagger para documentação da API.
- 🔲 Adicionar processamento assíncrono com Celery e Redis.
- 🔲 Melhorar cobertura de testes com Pytest.


## Licença

Este projeto está licenciado sob a licença MIT.

