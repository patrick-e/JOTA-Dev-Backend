from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import News
from user.models import ClientPlan
from datetime import datetime, timedelta


class NewsTests(APITestCase):
    def setUp(self):
        # Criar usuário Admin
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        self.admin_user.author_profile.role = "Admin"
        self.admin_user.author_profile.save()

        # Criar usuário Editor
        self.editor_user = User.objects.create_user(
            username='editor',
            email='editor@test.com',
            password='editor123'
        )
        self.editor_user.author_profile.role = "Editor"
        self.editor_user.author_profile.save()

        # Criar usuário Leitor PRO
        self.pro_user = User.objects.create_user(
            username='pro_reader',
            email='pro@test.com',
            password='pro123'
        )
        self.pro_user.author_profile.role = "Leitor"
        self.pro_user.author_profile.client_category = "PRO"
        self.pro_user.author_profile.save()

        # Criar plano PRO com verticais
        ClientPlan.objects.create(
            user=self.pro_user,
            is_pro=True,
            allowed_verticals=['poder', 'tributos']
        )

        # Criar notícia de teste
        self.news = News.objects.create(
            titulo="Teste",
            subtitulo="Subtítulo teste",
            conteudo="Conteúdo teste",
            data_de_publicacao=datetime.now().date(),
            autor=self.editor_user,
            status="published",
            categoria="poder",
            acesso="pro"
        )

    def test_admin_can_view_all_news(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('news-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), News.objects.count())

    def test_editor_can_create_news(self):
        self.client.force_authenticate(user=self.editor_user)
        data = {
            'titulo': 'Nova Notícia',
            'subtitulo': 'Subtítulo',
            'conteudo': 'Conteúdo',
            'data_de_publicacao': datetime.now().date(),
            'status': 'draft',
            'categoria': 'poder',
            'acesso': 'public'
        }
        response = self.client.post(reverse('news-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_pro_user_can_view_pro_news(self):
        self.client.force_authenticate(user=self.pro_user)
        response = self.client.get(reverse('news-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(n['acesso'] == 'pro' for n in response.data))

    def test_schedule_publication(self):
        tomorrow = datetime.now().date() + timedelta(days=1)
        news = News.objects.create(
            titulo="Agendada",
            subtitulo="Subtítulo",
            conteudo="Conteúdo",
            data_de_publicacao=tomorrow,
            autor=self.editor_user,
            status="draft",
            categoria="poder",
            acesso="public"
        )

        # Simular execução da tarefa agendada
        from .views import schedule_publication
        schedule_publication()

        # Verificar que a notícia não foi publicada (ainda não é amanhã)
        news.refresh_from_db()
        self.assertEqual(news.status, "draft")

    def test_editor_permissions(self):
        self.client.force_authenticate(user=self.editor_user)

        # Editor pode editar sua própria notícia
        response = self.client.patch(
            reverse('news-update', kwargs={'pk': self.news.pk}),
            {'titulo': 'Atualizado'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Criar outro editor
        other_editor = User.objects.create_user(
            username='other_editor',
            email='other@test.com',
            password='other123'
        )
        other_editor.author_profile.role = "Editor"
        other_editor.author_profile.save()

        # Criar notícia do outro editor
        other_news = News.objects.create(
            titulo="Outra",
            subtitulo="Subtítulo",
            conteudo="Conteúdo",
            data_de_publicacao=datetime.now().date(),
            autor=other_editor,
            status="published",
            categoria="poder",
            acesso="public"
        )

        # Editor não pode editar notícia de outro editor
        response = self.client.patch(
            reverse('news-update', kwargs={'pk': other_news.pk}),
            {'titulo': 'Atualizado'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
