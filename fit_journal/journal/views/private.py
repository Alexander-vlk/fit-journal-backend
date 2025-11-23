from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets, generics, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from auth_service.permissions import HasRefreshToken
from journal.models import Training, Exercise, ExerciseSet
from journal.serializers import TrainingRequestSerializer, TrainingResponseSerializer, ExerciseSetRequestSerializer, \
    ExerciseSetResponseSerializer, ExerciseSetIdRequestSerializer
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

        new_training = Training.objects.create(
            athlete=request.user,
            date=request_serializer.validated_data['date'],
        )
        exercises_in_training = Exercise.objects.filter(translit__in=request_serializer.validated_data['exercises_translit'])
        for exercise in exercises_in_training:
            new_training.exercises.add(exercise)

        response_serializer = TrainingResponseSerializer(instance=new_training)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


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

    def create(self, request, *args, **kwargs):
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

    def partial_update(self, request, *args, **kwargs):
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

    def destroy(self, request, *args, **kwargs):
        """Удалить подход"""
        request_serializer = ExerciseSetIdRequestSerializer(
            data={
                'id': kwargs['pk'],
            },
        )
        request_serializer.is_valid(raise_exception=True)
        get_object_or_404(ExerciseSet, id=request_serializer.validated_data['id']).delete()
        return Response(status=status.HTTP_200_OK)
