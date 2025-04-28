from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from editor.models import AuthorProfile
from .models import ClientPlan

@receiver(post_save, sender=User)
def create_user_profile_and_plan(sender, instance, created, **kwargs):
    """
    Signal para criar automaticamente o perfil do autor e plano do cliente
    quando um novo usuário é criado
    """
    if created:
        # Cria perfil do autor com role padrão
        AuthorProfile.objects.create(
            user=instance,
            nome_do_autor=instance.first_name,
            role="Leitor"
        )

        # Cria plano do cliente com configurações padrão
        ClientPlan.objects.create(
            user=instance,
            is_pro=False,
            allowed_verticals=[]
        )