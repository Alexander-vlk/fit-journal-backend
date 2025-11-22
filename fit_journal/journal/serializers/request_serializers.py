from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from journal.models import Exercise, ExerciseSet


@extend_schema_serializer(
    many=False,
    examples=[
        OpenApiExample(
            'Пример данных для запроса',
            value={
                'name': 'Тест',
            },
        ),
    ],
)
class ExerciseRequestSerializer(serializers.ModelSerializer):
    """Сериализатор запроса для модели Exercise"""

    class Meta:
        model = Exercise
        fields = [
            'name',
        ]


@extend_schema_serializer(
    many=False,
    examples=[
        OpenApiExample(
            'Стандартный формат запроса',
            value={
                'exercises_translit': [
                    'vypady',
                    'prised_so_shtangoj',
                ],
                'date': '2025-10-10',
            },
        ),
    ],
)
class TrainingRequestSerializer(serializers.Serializer):
    """Сериализатор запроса для модели Training"""

    exercises_translit = serializers.ListField(
        help_text='Список транслитов упражнений в тренировке',
        child=serializers.SlugField(),
        default=list,
    )
    date = serializers.DateField(
        help_text='Дата проведения тренировки',
        format='%Y-%m-%d',
    )


@extend_schema_serializer(
    many=True,
    examples=[
        OpenApiExample(
            'Стандартный запрос',
            value={
                'exercise_id': 1,
                'training_id': 1,
                'repetition': 12,
                'weight': 12,
                'comment': '',
            },
        ),
    ],
)
class ExerciseSetRequestSerializer(serializers.ModelSerializer):
    """Сериализатор подхода"""

    class Meta:
        model = ExerciseSet
        fields = [
            'exercise_id',
            'training_id',
            'repetition',
            'weight',
            'comment',
        ]
