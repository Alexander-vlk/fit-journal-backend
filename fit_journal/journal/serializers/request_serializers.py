from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from journal.models import Exercise, ExerciseSet, Training


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
    many=False,
    examples=[
        OpenApiExample(
            'Стандартный запрос',
            value={
                'id': 1,
            },
        ),
    ],
)
class ExerciseSetIdRequestSerializer(serializers.Serializer):
    """Сериализатор для ID подхода"""

    id = serializers.IntegerField(help_text='ID подхода', min_value=1)

    def validate_exercise_set_id(self, exercise_set_id):
        """Проверить, что удаляется подход, привязанный к тренировке пользователя"""
        if ExerciseSet.objects.select_related('training').get(id=exercise_set_id).training.user != self.context['user']:
            raise serializers.ValidationError('Нельзя удалить подход, привязанный к чужой тренировке')

        return exercise_set_id


@extend_schema_serializer(
    many=True,
    examples=[
        OpenApiExample(
            'Стандартный запрос',
            value={
                'training': 1,
                'exercise': 1,
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
            'exercise',
            'training',
            'repetition',
            'weight',
            'comment',
        ]

    def validate_training_id(self, training: int) -> int:
        """Проверить, что тренировка принадлежит пользователю, отправившему запрос"""
        if training not in Training.objects.filter(user=self.context['user']).values_list('id', flat=True):
            raise serializers.ValidationError('Нельзя создать тренировку другому пользователю')

        return training
