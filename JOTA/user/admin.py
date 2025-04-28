from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import ClientPlan
from editor.models import AuthorProfile

class AuthorProfileInline(admin.StackedInline):
    model = AuthorProfile
    can_delete = False
    verbose_name = 'Perfil de Autor'
    verbose_name_plural = 'Perfil de Autor'

class ClientPlanInline(admin.StackedInline):
    model = ClientPlan
    can_delete = False
    verbose_name = 'Plano do Cliente'
    verbose_name_plural = 'Plano do Cliente'
    fieldsets = (
        ('Informações do Plano', {
            'fields': ('is_pro', 'allowed_verticals')
        }),
    )

class CustomUserAdmin(UserAdmin):
    inlines = (AuthorProfileInline, ClientPlanInline)
    list_display = ('username', 'email', 'get_role', 'get_plan_type')
    list_filter = ('author_profile__role', 'client_plan__is_pro')
    
    def get_role(self, obj):
        try:
            return obj.author_profile.role
        except:
            return "Sem perfil"
    get_role.short_description = 'Função'
    
    def get_plan_type(self, obj):
        try:
            return "PRO" if obj.client_plan.is_pro else "Comum"
        except:
            return "Sem plano"
    get_plan_type.short_description = 'Tipo de Plano'

# Desregistrar o UserAdmin padrão e registrar o nosso customizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(ClientPlan)
class ClientPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_pro', 'get_allowed_verticals', 'get_user_role')
    list_filter = ('is_pro',)
    search_fields = ('user__username', 'user__author_profile__nome_do_autor')
    readonly_fields = ('user',)
    
    def get_allowed_verticals(self, obj):
        return ", ".join(obj.allowed_verticals) if obj.allowed_verticals else "Nenhuma"
    get_allowed_verticals.short_description = 'Verticais Permitidas'
    
    def get_user_role(self, obj):
        try:
            return obj.user.author_profile.role
        except:
            return "Sem perfil"
    get_user_role.short_description = 'Tipo de Usuário'