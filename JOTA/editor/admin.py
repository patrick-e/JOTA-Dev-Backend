from django.contrib import admin

# Register your models here.
from .models import News, AuthorProfile


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ('nome_do_autor', 'user')  # Exibe o nome do autor e o usuário vinculado
    search_fields = ('nome_do_autor', 'user__username')  # Permite busca por nome ou usuário

admin.site.register(News)