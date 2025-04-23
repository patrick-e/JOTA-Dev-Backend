## JOTA Backend Challenge
Este repositório contém a base inicial para o desenvolvimento do Case Backend - JOTA, proposto como parte de um processo seletivo. O objetivo é construir uma API RESTful utilizando Django, focando em escalabilidade, segurança e boas práticas de desenvolvimento.

## Objetivo do Projeto
Desenvolver uma API para a gestão de notícias, com suporte a diferentes perfis de usuários, autenticação JWT, agendamento de publicações e controle de acesso com base em planos contratados (JOTA Info e JOTA PRO). O sistema deve ser eficiente e escalável, utilizando processamento assíncrono para tarefas de longa duração.

## Estratégia Inicial
Antes da implementação, o foco está em garantir um planejamento sólido e aderente aos seguintes princípios:

Simplicidade e Clareza: Priorizando a entrega de soluções com arquiteturas simples, bem documentadas e com código legível.

Boas Práticas: Estruturação do projeto visando escalabilidade, testabilidade e manutenibilidade.

Explicação das Decisões: Cada escolha técnica será documentada e explicada com base em trade-offs, alinhada aos objetivos do case.

## Tecnologias e Ferramentas Propostas
Linguagem: Python 3.12+

Framework: Django + Django REST Framework

Banco de Dados: PostgreSQL

Autenticação: JWT (com djangorestframework-simplejwt)

Processamento Assíncrono: Celery + Redis

Documentação da API: Swagger (drf-yasg)

Containerização: Docker + Docker Compose

CI/CD: GitHub Actions

Testes: Pytest + coverage

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
## Próximos Passos
- Configuração inicial do ambiente com Django + PostgreSQL.

- Definição da arquitetura modular por domínio (apps isolados).

- Estruturação da autenticação JWT e perfis de acesso.

- Início da implementação dos endpoints de notícias.

