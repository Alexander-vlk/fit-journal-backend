from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from journal.models import Exercise
from journal.serializers import ExerciseResponseSerializer
from utils.constants import DefaultAPIResponses, APISchemaTags


@extend_schema(
    tags=[APISchemaTags.JOURNAL],
    summary='Получить данные из справочника упражнений',
    operation_id='Получить данные из справочника упражнений',
    responses={
        **DefaultAPIResponses.RESPONSES,
        status.HTTP_200_OK: ExerciseResponseSerializer,
    },
)
class ExerciseList(APIView):
    """Получить данные из справочника упражнений"""

    permission_classes: list = []
    authentication_classes: list = []

    @staticmethod
    def get(request):
        """GET-запрос"""
        serializer = ExerciseResponseSerializer(
            instance=Exercise.objects.all(),
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
