from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from journal.models import Exercise, Training, ExerciseSet, Color, AthleteTrainingTypeColor


@extend_schema_serializer(
    many=True,
    examples=[
        OpenApiExample(
            'Получение списка упражнений из справочника',
            value=[
                {
                    'id': 1,
                    'name': 'Выпады',
                    'translit': 'vypady',
                },
                {
                    'id': 2,
                    'name': 'Жим Арнольда',
                    'translit': 'zhim_rnolda',
                },
            ],
        ),
        OpenApiExample(
            'Получение одного упражнения из справочника',
            value={
                'id': 1,
                'name': 'Выпады',
                'translit': 'vypady',
            },
        ),
    ],
)
class ExerciseResponseSerializer(serializers.ModelSerializer):
    """Сериализатор модели Exercise"""

    class Meta:
        model = Exercise
        fields = [
            'id',
            'name',
            'translit',
        ]


@extend_schema_serializer(
    many=False,
    examples=[
        OpenApiExample(
            'Стандартный ответ',
            value={
                'id': 1,
                'athlete_id': 1,
                'exercises': [
                    {
                        'id': 1,
                        'name': 'Выпады',
                        'translit': 'vypady',
                    },
                    {
                        'id': 2,
                        'name': 'Жим Арнольда',
                        'translit': 'zhim_rnolda',
                    },
                ],
                'date': '2025-10-10',
            },
        ),
    ],
)
class TrainingResponseSerializer(serializers.ModelSerializer):
    """Сериализатор ответа для тренировки"""

    exercises = ExerciseResponseSerializer(help_text='Список упражнений в тренировке', many=True, read_only=True)

    class Meta:
        model = Training
        fields = [
            'id',
            'athlete_id',
            'exercises',
            'date',
        ]


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
class ExerciseSetResponseSerializer(serializers.ModelSerializer):
    """Сериализатор подхода"""

    class Meta:
        model = ExerciseSet
        fields = [
            'id',
            'exercise_id',
            'training_id',
            'repetition',
            'weight',
            'comment',
        ]


@extend_schema_serializer(
    many=True,
    examples=[
        OpenApiExample(
            'Стандартный ответ',
            value=[
                {
                    'id': 1,
                    'background_color': 'bg-blue-200',
                    'text_color': 'text-blue-700',
                },
                {
                    'id': 2,
                    'background_color': 'bg-red-200',
                    'text_color': 'text-red-700',
                },
                {
                    'id': 3,
                    'background_color': 'bg-green-200',
                    'text_color': 'text-green-700',
                },
            ],
        ),
    ],
)
class ColorResponseSerializer(serializers.ModelSerializer):
    """Сериализатор ответа для Color"""

    class Meta:
        model = Color
        fields = [
            'id',
            'background_color',
            'text_color',
        ]


@extend_schema_serializer(
    many=True,
    examples=[
        OpenApiExample(
            'Стандартный ответ',
            value=[
                {
                    'id': 1,
                    'background_color': 'bg-blue-200',
                    'text_color': 'text-blue-700',
                    'training_type': 'Фулбади',
                },
                {
                    'id': 2,
                    'background_color': 'bg-red-200',
                    'text_color': 'text-red-700',
                    'training_type': 'Грудь-трицепс',
                },
            ],
        ),
    ],
)
class AthleteTrainingTypeColorResponseSerializer(serializers.Serializer):
    """Сериализатор ответа для AthleteTrainingTypeColor"""

    id = serializers.IntegerField(help_text='ID записи', min_length=1)
    background_color = serializers.CharField(help_text='Цвет фона', max_length=30)
    text_color = serializers.CharField(help_text='Цвет текста', max_length=30)
    training_type = serializers.CharField(help_text='Тип тренировки', max_length=40)
