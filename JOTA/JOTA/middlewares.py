from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware para autenticação via JWT.
    """

    def __init__(self, get_response):
        super().__init__(get_response)
        self.jwt_auth = JWTAuthentication()

    def process_request(self, request):
        # Skip authentication for these paths
        if request.path in ['/register/', '/author/login/', '/author/token/refresh/', '/swagger/', '/redoc/']:
            return None

        try:
            # Get and validate JWT token
            header = request.META.get('HTTP_AUTHORIZATION', '')
            if not header.startswith('Bearer '):
                return JsonResponse({'error': 'Token não fornecido'}, status=401)

            validated_token = self.jwt_auth.get_validated_token(header.split(' ')[1])
            user = self.jwt_auth.get_user(validated_token)
            request.user = user

            # Check permissions for news API
            if request.path.startswith('/api/news/'):
                if not hasattr(user, 'author_profile'):
                    return JsonResponse({'error': 'Acesso negado: Permissão insuficiente'}, status=403)

        except Exception as e:
            request.user = AnonymousUser()
            return JsonResponse({'error': str(e)}, status=401)
