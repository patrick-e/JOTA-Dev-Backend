# JOTA Backend Challenge

Este repositório contém a base inicial para o desenvolvimento do Case Backend - JOTA, proposto como parte de um processo seletivo. O objetivo é construir uma API RESTful utilizando Django, focando em escalabilidade, segurança e boas práticas de desenvolvimento.

## Objetivo do Projeto

Desenvolver uma API para a gestão de notícias, com suporte a diferentes perfis de usuários, autenticação JWT, agendamento de publicações e controle de acesso com base em planos contratados (JOTA Info e JOTA PRO). O sistema deve ser eficiente e escalável, utilizando processamento assíncrono para tarefas de longa duração.

## Estratégia Inicial

Antes da implementação, o foco está em garantir um planejamento sólido e aderente aos seguintes princípios:

- **Simplicidade e Clareza**: Priorizando a entrega de soluções com arquiteturas simples, bem documentadas e com código legível.
- **Boas Práticas**: Estruturação do projeto visando escalabilidade, testabilidade e manutenibilidade.
- **Explicação das Decisões**: Cada escolha técnica será documentada e explicada com base em trade-offs, alinhada aos objetivos do case.

## Tecnologias e Ferramentas Propostas

- **Linguagem**: Python 3.12+
- **Framework**: Django + Django REST Framework
- **Banco de Dados**: PostgreSQL
- **Autenticação**: JWT (com djangorestframework-simplejwt)
- **Processamento Assíncrono**: Celery + Redis
- **Documentação da API**: Swagger (drf-yasg)
- **Containerização**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Testes**: Pytest + coverage

## Estrutura Inicial (Planejada)

```bash
jota/
├── manage.py
├── jota/                      # Configurações globais do projeto
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── noticias/                  # App responsável por CRUD de notícias
├── usuarios/                  # App responsável por autenticação e perfis
├── categorias/                # App opcional para verticalização das notícias
├── templates/ (se necessário)
├── static/ (se necessário)
└── README.md
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
   cp .env.example .env
   ```
   - Edite o arquivo `.env` se necessário para personalizar as configurações:
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
   
   **Nota**: Se você tiver o PostgreSQL instalado localmente, pode haver um conflito de porta. Nesse caso, temos duas opções:
   - Parar o serviço PostgreSQL local: `sudo systemctl stop postgresql`
   - Ou usar uma porta diferente no `docker-compose.yml` (já configurado para usar a porta 5433)

2. **Acesse o Adminer**:
   - Abra o navegador e acesse `http://localhost:8080`
   - Dados de conexão:
     - Sistema: PostgreSQL
     - Servidor: db
     - Usuário: definido em `.env` (padrão: admin)
     - Senha: definida em `.env` (padrão: 1234)
     - Base de dados: definida em `.env` (padrão: admin)

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
   - API (quando implementada): `http://localhost:8000/api/`

## Próximos Passos

- ✅ Configuração inicial do ambiente com Django + PostgreSQL.
- Definição da arquitetura modular por domínio (apps isolados).
- Estruturação da autenticação JWT e perfis de acesso.
- Início da implementação dos endpoints de notícias.

