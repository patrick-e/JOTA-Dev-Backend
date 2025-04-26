"""
URL configuration for JOTA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

# Configuração do Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="📚 JOTA API - Documentação Oficial",
        default_version="v1",
        description="""
Bem-vindo à API do JOTA!

Esta é a documentação interativa da API do JOTA, desenvolvida para gerenciar notícias e autenticação de usuários. Aqui você pode explorar os endpoints disponíveis, testar requisições e visualizar as respostas.

### Funcionalidades Principais:
- **Autenticação JWT:** Login seguro com tokens de acesso e renovação.
- **Gerenciamento de Notícias:** CRUD completo para criar, listar, atualizar e excluir notícias.
- **Controle de Acesso:** Diferenciação entre notícias públicas e restritas para usuários PRO.

### Como Usar:
1. Registre-se como usuário no endpoint `/register/`.
2. Faça login no endpoint `/author/login/` para obter seu token JWT.
3. Use o token para acessar os endpoints protegidos, como `/api/news/`.

### Endpoints Importantes:
- **Registro:** `POST /register/`
- **Login:** `POST /author/login/`
- **Listar Notícias:** `GET /api/news/`
- **Criar Notícia:** `POST /api/news/`
- **Atualizar Notícia:** `PATCH /api/news/update/<id>/`
- **Excluir Notícia:** `DELETE /api/news/delete/<id>/`

### Sobre o Projeto:
O JOTA é uma plataforma de notícias que visa oferecer informações confiáveis e organizadas. Este backend foi desenvolvido com foco em escalabilidade, segurança e boas práticas.

Desenvolvido com ❤️ por [Sua Equipe/Seu Nome]
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contato@jota.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("editor.urls")),  # Inclui as rotas do app editor
    path("", include("user.urls")),       # Inclui as rotas do app user
    path("author/login/", TokenObtainPairView.as_view(), name="author_login"),  # Rota de login do autor
    path("author/token/refresh/", TokenRefreshView.as_view(), name="author_token_refresh"),  # Rota de refresh do token

    # Rotas do Swagger
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),  # Removido o argumento 'layout'
        name="schema-swagger-ui"
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
