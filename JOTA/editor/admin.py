from django.contrib import admin
from .models import AuthorProfile, News
from django.contrib.auth.models import User


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ('nome_do_autor', 'user', 'role')
    list_filter = ('role',)
    search_fields = ('nome_do_autor', 'user__username')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            # Filtra apenas usuários que não têm um perfil de autor
            kwargs["queryset"] = User.objects.filter(author_profile__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        # Se estiver editando um objeto existente, user será somente leitura
        if obj:
            return ('user',)
        return ()


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'status', 'acesso', 'data_de_publicacao')
    list_filter = ('status', 'categoria', 'acesso')
    search_fields = ('titulo', 'subtitulo', 'autor__username')
    date_hierarchy = 'data_de_publicacao'
    readonly_fields = ('autor',)

    def save_model(self, request, obj, form, change):
        if not change:  # Se é uma nova notícia
            obj.autor = request.user
        super().save_model(request, obj, form, change)
