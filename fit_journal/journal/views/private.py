from drf_spectacular.utils import extend_schema
from rest_framework import generics, status

from journal.models import Exercise
from journal.serializers import ExerciseRequestSerializer
from utils.constants import DefaultAPIResponses, APISchemaTags


@extend_schema(
    tags=[APISchemaTags.JOURNAL],
    summary='Работа с записями в справочнике упражнений',
    operation_id='Изменить/удалить/создать запись в справочнике упражнений',
    responses={
        **DefaultAPIResponses.RESPONSES,
        status.HTTP_201_CREATED: ExerciseRequestSerializer,
    },
)
class ExerciseChangeView(generics.CreateAPIView):
    """Изменить/удалить/создать запись в справочник упражнений"""

    permission_classes = []
    authentication_classes = []
    serializer_class = ExerciseRequestSerializer
    queryset = Exercise.objects.all()
