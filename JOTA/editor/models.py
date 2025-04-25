from django.db import models
from django.contrib.auth.models import User

class AuthorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="author_profile")
    nome_do_autor = models.CharField(max_length=300)

    def __str__(self):
        return self.nome_do_autor

class News(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
    ]

    ACCESS_CHOICES = [
        ('public', 'Público'),
        ('pro', 'Restrito a PRO'),
    ]

    CATEGORY_CHOICES = [
        ('poder', 'Poder'),
        ('tributos', 'Tributos'),
        ('saude', 'Saúde'),
        ('energia', 'Energia'),
        ('trabalhista', 'Trabalhista'),
    ]

    titulo = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='news_images/', null=True, blank=True)
    conteudo = models.TextField()
    data_de_publicacao = models.DateField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="news")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    categoria = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default='poder')
    acesso = models.CharField(max_length=10, choices=ACCESS_CHOICES, default='public')

    def __str__(self):
        return self.titulo