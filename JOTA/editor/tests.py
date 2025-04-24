from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status
from PIL import Image
import io
from .models import News

class NewsUpdateTestCase(APITestCase):
    def setUp(self):
        # Criar uma imagem teste inicial
        image = Image.new('RGB', (100, 100), color='blue')
        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        initial_image = SimpleUploadedFile("test_image.jpg", img_io.read(), content_type="image/jpeg")

        self.news = News.objects.create(
            titulo="Notícia Teste",
            subtitulo="Subtítulo Teste",
            conteudo="Conteúdo Teste",
            data_de_publicacao="2023-10-01",
            autor="Autor Teste",
            status="draft",
            categoria="poder",
            acesso="public",
            imagem=initial_image,
        )

    def test_update_without_image(self):
        response = self.client.patch(f"/api/news/update/{self.news.id}", {
            "titulo": "Título Atualizado"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.news.refresh_from_db()
        self.assertEqual(self.news.titulo, "Título Atualizado")
        self.assertIsNotNone(self.news.imagem)  # A imagem antiga deve ser mantida

    def test_update_with_new_image(self):
        # Criar uma imagem teste usando PIL
        image = Image.new('RGB', (100, 100), color='red')
        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        new_image = SimpleUploadedFile("new_image.jpg", img_io.read(), content_type="image/jpeg")
        response = self.client.patch(f"/api/news/update/{self.news.id}", {
            "imagem": new_image
        }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.news.refresh_from_db()
        self.assertEqual(self.news.imagem.name, "news_images/new_image.jpg")  # Verifica se a nova imagem foi salva
