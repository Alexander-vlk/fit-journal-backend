from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from auth_service.permissions import HasNoRefreshToken
from auth_service.services import get_authenticated_response
from utils.constants import APISchemaTags, DefaultAPIResponses


@extend_schema(
    tags=[APISchemaTags.AUTH_SERVICE],
    summary='Проверка доступности сервиса',
    operation_id='Проверка доступности сервиса',
    responses=DefaultAPIResponses.RESPONSES,
)
class HealthCheck(APIView):
    """Проверка доступности сервиса"""

    authentication_classes: list = []
    permission_classes: list = []

    @staticmethod
    def get(request):
        """GET-запрос"""
        return Response(status=status.HTTP_200_OK)


@extend_schema(
    tags=[APISchemaTags.AUTH_SERVICE],
    summary='Получить пару access и refresh токенов',
    operation_id='Получение пары токенов',
    responses={
        **DefaultAPIResponses.RESPONSES,
        status.HTTP_200_OK: TokenObtainPairSerializer,
    },
)
class CustomTokenObtainPairView(TokenObtainPairView):
    """Получить пару access и refresh токенов"""

    permission_classes: list = [HasNoRefreshToken]
    authentication_classes: list = []

    def post(self, request, *args, **kwargs):
        """POST-запрос"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access_token = serializer.validated_data['access']
        refresh_token = serializer.validated_data['refresh']

        response = get_authenticated_response(request, access_token, refresh_token)
        return response
