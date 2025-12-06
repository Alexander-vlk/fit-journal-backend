from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from journal.models import (
    Exercise,
    Training,
    ExerciseSet,
    Color,
    TrainingType,
    AthleteTrainingTypeColor,
)


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
    many=True,
    examples=[
        OpenApiExample(
            'Стандартный ответ',
            value=[
                {
                    'id': 1,
                    'name': 'Грудь-трицепс',
                },
                {
                    'id': 2,
                    'name': 'Спина-бицепс',
                },
            ],
        ),
    ],
)
class TrainingTypeResponseSerializer(serializers.ModelSerializer):
    """Сериализатор модели TrainingType"""

    class Meta:
        model = TrainingType
        fields = [
            'id',
            'name',
        ]


@extend_schema_serializer(
    many=True,
    examples=[
        OpenApiExample(
            'Стандартный ответ',
            value=[
                {
                    'id': 1,
                    'name': 'Синий',
                    'background_color': 'bg-blue-200',
                    'text_color': 'text-blue-700',
                },
                {
                    'id': 2,
                    'name': 'Красный',
                    'background_color': 'bg-red-200',
                    'text_color': 'text-red-700',
                },
                {
                    'id': 3,
                    'name': 'Зеленый',
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
            'name',
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
                    'training_type': 'Фулбади',
                    'color': {
                        'name': 'Красный',
                        'background_color': 'bg-red-200',
                        'text_color': 'text-red-700',
                    },
                },
                {
                    'id': 2,
                    'training_type': 'Грудь-трицепс',
                    'color': {
                        'name': 'Синий',
                        'background_color': 'bg-blue-200',
                        'text_color': 'text-blue-700',
                    },
                },
            ],
        ),
    ],
)
class AthleteTrainingTypeColorResponseSerializer(serializers.ModelSerializer):
    """Сериализатор ответа для AthleteTrainingTypeColor"""

    training_type = TrainingTypeResponseSerializer(help_text='Тип тренировки')
    color = ColorResponseSerializer(help_text='Цвет')

    class Meta:
        model = AthleteTrainingTypeColor
        fields = [
            'id',
            'athlete',
            'training_type',
            'color',
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
                'training_type_color': {
                    'id': 2,
                    'training_type': {
                        'id': 1,
                        'name': 'Грудь-трицепс',
                    },
                    'color': {
                        'name': 'Синий',
                        'background_color': 'bg-blue-200',
                        'text_color': 'text-blue-700',
                    },
                },
            },
        ),
    ],
)
class TrainingResponseSerializer(serializers.ModelSerializer):
    """Сериализатор ответа для тренировки"""

    exercises = ExerciseResponseSerializer(
        help_text='Список упражнений в тренировке', many=True, read_only=True
    )
    athlete_training_type = AthleteTrainingTypeColorResponseSerializer(
        help_text='Связь Спортсмен - Тип тренировки - Цвет',
        read_only=True,
    )

    class Meta:
        model = Training
        fields = [
            'id',
            'athlete_id',
            'exercises',
            'athlete_training_type',
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
