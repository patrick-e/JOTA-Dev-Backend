from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Configuração do Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API do JOTA",
        default_version='v1',
        description="""
        API do JOTA para gerenciamento de notícias e conteúdo.

        ## Recursos Principais
        - Gerenciamento completo de notícias (CRUD)
        - Sistema de autenticação JWT
        - Diferentes níveis de acesso (Admin, Editor, Leitor)
        - Agendamento de publicações
        - Análise de métricas de leitura
        """,
        terms_of_service="https://www.jota.info/termos-de-uso",
        contact=openapi.Contact(email="contato@jota.info"),
        license=openapi.License(name="Proprietary"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# URLs do projeto
urlpatterns = [
    # Endpoints de autenticação
    path('api/v1/auth/', include('user.urls')),

    # Endpoints de notícias e análises
    path('api/v1/', include('editor.urls')),

    # Admin interface
    path('admin/', admin.site.urls),

    # Documentação Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Configuração para servir arquivos estáticos e de mídia em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
