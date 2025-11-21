from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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

    def get(self, request):
        """GET-запрос"""
        return Response(status=status.HTTP_200_OK)
