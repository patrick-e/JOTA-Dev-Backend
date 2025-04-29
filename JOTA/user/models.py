from django.db import models
from django.contrib.auth.models import User


class ClientPlan(models.Model):
    VERTICAL_CHOICES = [
        ('poder', 'Poder'),
        ('tributos', 'Tributos'),
        ('saude', 'Saúde'),
        ('energia', 'Energia'),
        ('trabalhista', 'Trabalhista'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_plan')
    allowed_verticals = models.JSONField(default=list)  # Lista de verticais permitidas
    is_pro = models.BooleanField(default=False)

    def has_access_to_vertical(self, vertical):
        return vertical in self.allowed_verticals if self.is_pro else False

    def __str__(self):
        return f"{self.user.username} - {'PRO' if self.is_pro else 'Comum'}"
