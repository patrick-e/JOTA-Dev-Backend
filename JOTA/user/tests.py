from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class UserTests(APITestCase):
    def setUp(self):
        # Criação de um usuário comum
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="Test@1234"
        )
        # Criação de um superusuário
        self.admin_user = User.objects.create_superuser(
            username="adminuser",
            email="adminuser@example.com",
            password="Admin@1234"
        )
        # URL dos endpoints
        self.register_url = reverse('user:register')
        self.login_url = reverse('user:token_obtain_pair')
        self.refresh_url = reverse('user:token_refresh')
        self.profile_url = reverse('user:user_profile')

    def test_register_user(self):
        """Teste para registrar um novo usuário"""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "NewUser@1234",
            "first_name": "New",
            "last_name": "User",
            "role": "Leitor",
            "is_pro": False,
            "allowed_verticals": []
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["username"], "newuser")

    def test_register_user_with_existing_username(self):
        """Teste para registrar um usuário com nome de usuário já existente"""
        data = {
            "username": "testuser",
            "email": "duplicate@example.com",
            "password": "Duplicate@1234"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_login_user(self):
        """Teste para login de um usuário existente"""
        data = {
            "username": "testuser",
            "password": "Test@1234"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        """Teste para login com credenciais inválidas"""
        data = {
            "username": "testuser",
            "password": "WrongPassword"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_refresh_token(self):
        """Teste para atualizar o token JWT"""
        login_data = {
            "username": "testuser",
            "password": "Test@1234"
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        refresh_token = login_response.data["refresh"]

        refresh_data = {"refresh": refresh_token}
        response = self.client.post(self.refresh_url, refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_update_user_profile(self):
        """Teste para atualizar o perfil do usuário"""
        self.client.force_authenticate(user=self.user)
        update_data = {
            "email": "updateduser@example.com",
            "password": "Updated@1234"
        }
        response = self.client.patch(self.profile_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "updateduser@example.com")

    def test_admin_can_view_all_users(self):
        """Teste para verificar se o admin pode visualizar todos os usuários"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)  # Admin e usuário comum

    def test_user_cannot_access_admin_endpoints(self):
        """Teste para verificar se um usuário comum pode visualizar apenas seu próprio perfil"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
