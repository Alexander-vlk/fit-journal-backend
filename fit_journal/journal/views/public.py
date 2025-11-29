from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from journal.models import Exercise, Color
from journal.serializers import ExerciseResponseSerializer, ColorResponseSerializer
from utils.constants import DefaultAPIResponses, APISchemaTags


@extend_schema_view(
    retrieve=extend_schema(
        tags=[APISchemaTags.JOURNAL],
        summary='Получить запись из справочника тренировок',
        operation_id='Получить запись из справочника тренировок',
        responses={
            **DefaultAPIResponses.RESPONSES,
            status.HTTP_200_OK: ExerciseResponseSerializer,
        },
    ),
    list=extend_schema(
        tags=[APISchemaTags.JOURNAL],
        summary='Получить список записей из справочника тренировок',
        operation_id='Получить список записей из справочника тренировок',
        responses={
            **DefaultAPIResponses.RESPONSES,
            status.HTTP_200_OK: ExerciseResponseSerializer,
        },
    ),
)
class ExerciseViewSet(generics.ListAPIView, generics.RetrieveAPIView, viewsets.GenericViewSet):
    """Получить данные из справочника упражнений"""

    permission_classes: list = []
    authentication_classes: list = []
    lookup_field = 'translit'
    queryset = Exercise.objects.all()
    serializer_class = ExerciseResponseSerializer


@extend_schema_view(
    get=extend_schema(
        tags=[APISchemaTags.JOURNAL],
        summary='Получить список записей из справочника цветовых схем',
        operation_id='Получить список записей из справочника цветовых схем',
        responses={
            **DefaultAPIResponses.RESPONSES,
            status.HTTP_200_OK: ColorResponseSerializer,
        },
    ),
)
class GetColorsList(APIView):
    """Получить список доступных цветовых схем"""

    permission_classes: list = []
    authentication_classes: list = []

    @staticmethod
    def get(request):
        """GET-запрос"""
        response_serializer = ColorResponseSerializer(
            instance=Color.objects.all(),
            many=True,
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)
