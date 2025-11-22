from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from journal.models import Exercise


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
