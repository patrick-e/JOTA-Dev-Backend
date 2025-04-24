from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status
from .models import News
import tempfile
from PIL import Image

class NewsAPITestCase(APITestCase):
    def setUp(self):
        self.news = News.objects.create(
            titulo="Notícia Teste",
            subtitulo="Subtítulo Teste",
            conteudo="Conteúdo Teste",
            data_de_publicacao="2023-10-01",
            autor="Autor Teste",
            status="draft",
            categoria="poder",
            acesso="public",
        )

    def generate_image_file(self):
        """Gera um arquivo de imagem temporário para o teste."""
        image = Image.new('RGB', (100, 100), color='red')
        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(temp_file, format='JPEG')
        temp_file.seek(0)
        return temp_file

    def test_list_news(self):
        response = self.client.get("/api/news/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_news(self):
        image_file = self.generate_image_file()
        image = SimpleUploadedFile("test_image.jpg", image_file.read(), content_type="image/jpeg")
        data = {
            "titulo": "Nova Notícia",
            "subtitulo": "Novo Subtítulo",
            "conteudo": "Novo Conteúdo",
            "data_de_publicacao": "2023-10-02",
            "autor": "Novo Autor",
            "status": "draft",
            "categoria": "tributos",
            "acesso": "pro",
            "imagem": image,
        }
        response = self.client.post("/api/news/", data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
