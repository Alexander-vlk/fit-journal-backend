from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheck(APIView):
    """Проверка доступности сервиса"""

    authentication_classes: list = []
    permission_classes: list = []

    def get(self, request):
        """GET-запрос"""
        return Response(status.HTTP_200_OK)\
