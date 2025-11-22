from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from journal.models import Training, Exercise
from journal.serializers import TrainingRequestSerializer, TrainingResponseSerializer
from utils.constants import DefaultAPIResponses, APISchemaTags


@extend_schema(
    tags=[APISchemaTags.JOURNAL],
    summary='Создать тренировку',
    operation_id='Создать тренировку',
    request=TrainingRequestSerializer,
    responses={
        **DefaultAPIResponses.RESPONSES,
        status.HTTP_201_CREATED: TrainingResponseSerializer,
    },
)
class TrainingCreate(APIView):
    """Создать тренировку"""

    permission_classes: list = [IsAuthenticated]
    authentication_classes: list = [JWTAuthentication]

    @staticmethod
    def post(request, *args, **kwargs):
        """POST-запрос"""
        request_serializer = TrainingRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        new_training = Training.objects.create(
            athlete=request.user,
            date=request_serializer.validated_data['date'],
        )
        exercises_in_training = Exercise.objects.filter(translit__in=request_serializer.validated_data['exercises_translit'])
        for exercise in exercises_in_training:
            new_training.exercises.add(exercise)

        response_serializer = TrainingResponseSerializer(instance=new_training)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
