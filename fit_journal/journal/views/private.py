from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from auth_service.permissions import HasRefreshToken
from journal.models import Training, Exercise, ExerciseSet, AthleteTrainingTypeColor, TrainingType, Color
from journal.serializers import (
    TrainingRequestSerializer,
    TrainingResponseSerializer,
    ExerciseSetRequestSerializer,
    ExerciseSetIdRequestSerializer,
    AthleteTrainingTypeColorResponseSerializer,
)
from utils.constants import DefaultAPIResponses, APISchemaTags


@extend_schema_view(
    post=extend_schema(
        tags=[APISchemaTags.JOURNAL],
        summary='Создать тренировку',
        operation_id='Создать тренировку',
        request=TrainingRequestSerializer,
        responses={
            **DefaultAPIResponses.RESPONSES,
            status.HTTP_201_CREATED: TrainingResponseSerializer,
        },
    ),
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

        new_athlete_training_type_color = AthleteTrainingTypeColor.objects.create(
            athlete=request.user,
            training_type=get_object_or_404(TrainingType, name=request_serializer.validated_data['training_type']),
            color=get_object_or_404(Color, name=request_serializer.validated_data['color']),
        )
        new_training = Training.objects.create(
            athlete=request.user,
            date=request_serializer.validated_data['date'],
            athlete_training_type=new_athlete_training_type_color,
        )
        exercises_in_training = Exercise.objects.filter(
            translit__in=request_serializer.validated_data['exercises_translit'],
        )
        for exercise in exercises_in_training:
            new_training.exercises.add(exercise)

        response_serializer = TrainingResponseSerializer(instance=new_training)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    list=extend_schema(
        tags=[APISchemaTags.JOURNAL],
        summary='Получить список связей Атлет - Тип тренировки - Цвет',
        operation_id='Получить список связей Атлет - Тип тренировки - Цвет',
    ),
    retrieve=extend_schema(
        tags=[APISchemaTags.JOURNAL],
        summary='Получить связь Атлет - Тип тренировки - Цвет',
        operation_id='Получить связь Атлет - Тип тренировки - Цвет',
    ),
    create=extend_schema(
        tags=[APISchemaTags.JOURNAL],
        summary='Создать связь Атлет - Тип тренировки - Цвет',
        operation_id='Создать связь Атлет - Тип тренировки - Цвет',
    ),
    update=extend_schema(
        tags=[APISchemaTags.JOURNAL],
        summary='Обновить связь Атлет - Тип тренировки - Цвет',
        operation_id='Обновить связь Атлет - Тип тренировки - Цвет',
    ),
    destroy=extend_schema(
        tags=[APISchemaTags.JOURNAL],
        summary='Удалить связь Атлет - Тип тренировки - Цвет',
        operation_id='Удалить связь Атлет - Тип тренировки - Цвет',
    ),
)
class AthleteTrainingTypeColorViewSet(viewsets.ViewSet):
    """CRUD для AthleteTrainingTypeColor"""

    permission_classes: list = [IsAuthenticated]
    authentication_classes: list = [JWTAuthentication]

    @staticmethod
    def list(request):
        """Получить список связей AthleteTrainingTypeColor для конкретного пользователя"""
        relations = (
            AthleteTrainingTypeColor.objects.filter(athlete=request.user)
            .select_related('color', 'training_type')
        )
        response_serializer = AthleteTrainingTypeColorResponseSerializer(instance=relations, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def retrieve(request, pk):
        """Получить связь AthleteTrainingTypeColor для конкретного пользователя"""
        relation = (
            AthleteTrainingTypeColor.objects.filter(athlete=request.user, pk=pk)
            .select_related('color', 'training_type')
            .first()
        )
        if not relation:
            return Response(status=status.HTTP_404_NOT_FOUND)

        response_serializer = AthleteTrainingTypeColorResponseSerializer(instance=relation)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        """Создать связь AthleteTrainingTypeColor"""

    @staticmethod
    def update(request, pk):
        """Частично обновить связь AthleteTrainingTypeColor"""

    @staticmethod
    def destroy(request, pk):
        """Удалить связь AthleteTrainingTypeColor"""


@extend_schema_view(
    create=extend_schema(
        tags=[APISchemaTags.JOURNAL],
        summary='Создать подход',
        operation_id='Создать подход',
        request=ExerciseSetRequestSerializer,
        responses={
            **DefaultAPIResponses.RESPONSES,
            status.HTTP_201_CREATED: {},
        },
    ),
    partial_update=extend_schema(
        tags=[APISchemaTags.JOURNAL],
        summary='Обновить подход',
        operation_id='Обновить подход',
        request=ExerciseSetRequestSerializer,
        responses={
            **DefaultAPIResponses.RESPONSES,
            status.HTTP_200_OK: {},
        },
    ),
    destroy=extend_schema(
        tags=[APISchemaTags.JOURNAL],
        summary='Удалить подход',
        operation_id='Удалить подход',
        request=ExerciseSetRequestSerializer,
        responses={
            **DefaultAPIResponses.RESPONSES,
            status.HTTP_200_OK: {},
        },
    ),
)
class ExerciseSetViewSet(viewsets.ViewSet):
    """CRUD для подхода к упражнению"""

    permission_classes = [IsAuthenticated, HasRefreshToken]
    authentication_classes = [JWTAuthentication]

    @staticmethod
    def create(request, *args, **kwargs):
        """Создать подход"""
        request_serializer = ExerciseSetRequestSerializer(
            data=request.data,
            context={
                'user': request.user,
            },
        )
        request_serializer.is_valid(raise_exception=True)
        request_serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def partial_update(request, *args, **kwargs):
        """Обновить подход"""
        exercise_set = get_object_or_404(ExerciseSet, id=kwargs['pk'])
        request_serializer = ExerciseSetRequestSerializer(
            exercise_set,
            data=request.data,
            context={
                'user': request.user,
            },
            partial=True,
        )
        request_serializer.is_valid(raise_exception=True)
        request_serializer.save()
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def destroy(request, *args, **kwargs):
        """Удалить подход"""
        request_serializer = ExerciseSetIdRequestSerializer(
            data={
                'id': kwargs['pk'],
            },
        )
        request_serializer.is_valid(raise_exception=True)
        get_object_or_404(ExerciseSet, id=request_serializer.validated_data['id']).delete()
        return Response(status=status.HTTP_200_OK)
