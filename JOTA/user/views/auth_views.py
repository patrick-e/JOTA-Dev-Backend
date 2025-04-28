from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from ..serializers import UserCreateSerializer, UserDetailSerializer
from ..services import AuthService

class LoginView(TokenObtainPairView):
    """
    Endpoint para login de usuários.
    
    post:
    Autentica um usuário e retorna tokens JWT.
    
    Parâmetros:
    - username: Nome de usuário
    - password: Senha
    
    Retorna:
    - access: Token de acesso JWT
    - refresh: Token de atualização JWT
    
    Possíveis códigos de resposta:
    - 200: Login realizado com sucesso
    - 401: Credenciais inválidas
    """
    pass

class RefreshTokenView(TokenRefreshView):
    """
    Endpoint para atualização de token JWT.
    
    post:
    Gera um novo token de acesso usando um token de atualização.
    
    Parâmetros:
    - refresh: Token de atualização JWT válido
    
    Retorna:
    - access: Novo token de acesso JWT
    
    Possíveis códigos de resposta:
    - 200: Token atualizado com sucesso
    - 401: Token de atualização inválido ou expirado
    """
    pass

class RegisterView(generics.CreateAPIView):
    """
    Endpoint para registro de novos usuários.
    
    create:
    Registra um novo usuário no sistema.
    
    Parâmetros:
    - username: Nome de usuário único
    - email: Email válido
    - password: Senha
    - first_name: Nome (opcional)
    - last_name: Sobrenome (opcional)
    
    Retorna:
    - Dados do usuário criado
    - Tokens de acesso JWT (se autenticação automática estiver ativada)
    
    Possíveis códigos de resposta:
    - 201: Usuário criado com sucesso
    - 400: Dados inválidos ou usuário já existe
    - 500: Erro interno do servidor
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Usa o serviço de autenticação para criar o usuário
            user, tokens = AuthService.create_user(serializer.validated_data)
            
            # Retorna os dados do usuário e tokens se disponíveis
            response_data = {
                "user": UserDetailSerializer(user).data
            }
            
            if tokens:
                response_data.update(tokens)
            else:
                response_data["message"] = "Usuário registrado, mas sem autenticação automática."
                
            return Response(response_data)
            
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)
        except Exception as e:
            return Response(
                {"error": "Erro ao registrar usuário. Por favor, tente novamente."},
                status=500
            )