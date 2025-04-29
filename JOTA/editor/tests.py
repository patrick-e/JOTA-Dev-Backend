from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import News
from user.models import ClientPlan
from datetime import datetime, timedelta
from editor.services import NewsService  # Importar o serviço correto


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
        self.pro_user.author_profile.save()

        # Garantir que o usuário tem um plano PRO ativo
        print("\nDEBUG - Configurando plano PRO:")
        ClientPlan.objects.filter(user=self.pro_user).delete()  # Remover plano existente
        client_plan = ClientPlan.objects.create(
            user=self.pro_user,
            is_pro=True,
            allowed_verticals=['poder', 'tributos']
        )

        # Forçar refresh do plano
        client_plan.refresh_from_db()
        print(f"Plano criado: is_pro={client_plan.is_pro}, verticais={client_plan.allowed_verticals}")

        # Forçar refresh do usuário para garantir que o plano está associado
        self.pro_user.refresh_from_db()

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
        response = self.client.get(reverse('editor:news-list'))  # Adicionado namespace
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), News.objects.count())

    def test_editor_can_create_news(self):
        self.client.force_authenticate(user=self.editor_user)
        data = {
            'titulo': 'Nova Notícia',
            'subtitulo': 'Subtítulo',
            'conteudo': 'Conteúdo com mais de 50 caracteres para passar na validação.',
            'data_de_publicacao': datetime.now().date(),
            'status': 'draft',
            'categoria': 'poder',
            'acesso': 'public'
        }
        response = self.client.post(reverse('editor:news-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_pro_user_can_view_pro_news(self):
        # Autenticar usuário PRO e verificar suas informações
        self.client.force_authenticate(user=self.pro_user)
        print("\nDEBUG - Usuário autenticado:")
        print(f"ID: {self.pro_user.id}")
        print(f"Username: {self.pro_user.username}")
        print(f"Tem plano PRO: {hasattr(self.pro_user, 'client_plan')}")
        if hasattr(self.pro_user, 'client_plan'):
            print(f"Plano PRO ativo: {self.pro_user.client_plan.is_pro}")
            print(f"Verticais permitidas: {self.pro_user.client_plan.allowed_verticals}")

        pro_news = News.objects.create(
            titulo="Notícia PRO",
            subtitulo="Subtítulo PRO",
            conteudo="Conteúdo de teste para notícia PRO" * 10,
            data_de_publicacao=datetime.now().date(),
            autor=self.editor_user,
            status="published",  # Explicitamente definido como published
            categoria="poder",  # categoria permitida para o usuário PRO
            acesso="pro"
        )

        # Forçar refresh do objeto para garantir que foi salvo corretamente
        pro_news.refresh_from_db()
        print("\nDEBUG - Notícia PRO criada:")
        print(f"ID: {pro_news.id}")
        print(f"Título: {pro_news.titulo}")
        print(f"Categoria: {pro_news.categoria}")
        print(f"Status: {pro_news.status}")
        print(f"Acesso: {pro_news.acesso}")

        response = self.client.get(reverse('editor:news-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        print("\nDEBUG - Resposta da API:")
        print(f"Total de notícias na resposta: {len(response.data)}")
        print("Notícias na resposta:")
        for news in response.data:
            print(f"- Título: {news['titulo']}")
            print(f"  Categoria: {news['categoria']}")
            print(f"  Acesso: {news['acesso']}")
            print(f"  Status: {news['status']}")

        # Verificar se existe pelo menos uma notícia com acesso PRO na resposta
        pro_news_in_response = any(n['acesso'] == 'pro' for n in response.data)
        self.assertTrue(pro_news_in_response, "Usuário PRO não conseguiu acessar notícia PRO")

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
        NewsService.publish_scheduled_news()  # Usar o método correto do serviço

        # Verificar que a notícia não foi publicada (ainda não é amanhã)
        news.refresh_from_db()
        self.assertEqual(news.status, "draft")

    def test_editor_permissions(self):
        self.client.force_authenticate(user=self.editor_user)

        # Editor pode editar sua própria notícia
        response = self.client.patch(
            reverse('editor:news-update', kwargs={'pk': self.news.pk}),  # Adicionado namespace
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
            reverse('editor:news-update', kwargs={'pk': other_news.pk}),
            {'titulo': 'Atualizado'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        User.objects.all().delete()
        ClientPlan.objects.all().delete()
        News.objects.all().delete()
