from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from journal.models import Exercise


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
                'athlete_id': 123,
                'exercises_translit': [
                    'vypady',
                    'prised_so_shtangoy',
                ],
                'date': '2025-10-10',
            },
        ),
    ],
)
class TrainingRequestSerializer(serializers.Serializer):
    """Сериализатор запроса для модели Training"""

    athlete_id = serializers.IntegerField(help_text='ID спортсмена', min_value=1)
    exercises_translit = serializers.ListField(
        help_text='Список транслитов упражнений в тренировке',
        child=serializers.SlugField(),
        default=list,
    )
    date = serializers.DateField(
        help_text='Дата проведения тренировки',
        format='%Y-%m-%d',
    )
