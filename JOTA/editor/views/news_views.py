from rest_framework import generics, filters
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters import rest_framework as django_filters
from django.core.cache import cache
from ..models import News
from ..serializers import NewsSerializers
from ..services import NewsService
from user.permissions import IsAdmin, IsEditor, IsProUser, ReadOnly

class NewsFilter(django_filters.FilterSet):
    categoria = django_filters.CharFilter(lookup_expr='iexact')
    status = django_filters.CharFilter(lookup_expr='iexact')
    acesso = django_filters.CharFilter(lookup_expr='iexact')
    data_inicio = django_filters.DateFilter(field_name='data_de_publicacao', lookup_expr='gte')
    data_fim = django_filters.DateFilter(field_name='data_de_publicacao', lookup_expr='lte')
    
    class Meta:
        model = News
        fields = ['categoria', 'status', 'acesso', 'data_inicio', 'data_fim']

class NewsList(generics.ListCreateAPIView):
    """
    Listagem e criação de notícias.
    
    list:
    Retorna uma lista paginada de todas as notícias acessíveis ao usuário.
    Suporta filtros por categoria, status e tipo de acesso.
    
    create:
    Cria uma nova notícia. Requer autenticação como Admin ou Editor.
    """
    serializer_class = NewsSerializers
    permission_classes = [IsAuthenticated | ReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NewsFilter
    search_fields = ['titulo', 'conteudo', 'categoria']
    ordering_fields = ['data_de_publicacao', 'data_de_criacao', 'titulo']
    ordering = ['-data_de_publicacao']

    def get_queryset(self):
        page = self.request.query_params.get('page', 1)
        try:
            return NewsService.get_news_queryset(self.request.user, page=int(page))
        except ValueError:
            raise ValidationError("Número de página inválido")

    def perform_create(self, serializer):
        if not (IsAdmin().has_permission(self.request, self) or 
                IsEditor().has_permission(self.request, self)):
            raise ValidationError("Apenas administradores e editores podem criar notícias")
        try:
            NewsService.create_news(serializer.validated_data, self.request.user)
        except ValidationError as e:
            raise ValidationError(str(e))

class NewsDetail(generics.RetrieveDestroyAPIView):
    """
    Recuperação e exclusão de notícias específicas.
    
    retrieve:
    Retorna os detalhes de uma notícia específica.
    Registra a visualização da notícia para análise.
    
    destroy:
    Exclui uma notícia. Requer autenticação como Admin ou Editor (proprietário).
    """
    serializer_class = NewsSerializers
    permission_classes = [IsAuthenticated | ReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        return NewsService.get_news_queryset(self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            NewsService.view_news(instance.id, request.user.id)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            raise ValidationError(f"Erro ao recuperar notícia: {str(e)}")

    def destroy(self, request, *args, **kwargs):
        if not (IsAdmin().has_permission(request, self) or 
                (IsEditor().has_permission(request, self) and 
                 self.get_object().autor == request.user)):
            raise ValidationError("Você não tem permissão para excluir esta notícia")
        try:
            NewsService.delete_news(self.get_object().id)
            return Response(status=204)
        except Exception as e:
            raise ValidationError(f"Erro ao excluir notícia: {str(e)}")

class NewsUpdate(generics.RetrieveUpdateAPIView):
    """
    Atualização de notícias.
    
    retrieve:
    Retorna os detalhes de uma notícia para edição.
    
    update:
    Atualiza uma notícia existente. Requer autenticação como Admin ou Editor (proprietário).
    Suporta atualização parcial via PATCH.
    """
    serializer_class = NewsSerializers
    permission_classes = [IsAdmin | IsEditor]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        if IsAdmin().has_permission(self.request, self):
            return News.objects.all()
        return News.objects.filter(autor=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not (IsAdmin().has_permission(request, self) or 
                (IsEditor().has_permission(request, self) and 
                 instance.autor == request.user)):
            raise ValidationError("Você não tem permissão para editar esta notícia")
        
        try:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_instance = NewsService.update_news(instance, serializer.validated_data)
            return Response(self.get_serializer(updated_instance).data)
        except ValidationError as e:
            raise ValidationError(f"Erro ao atualizar notícia: {str(e)}")