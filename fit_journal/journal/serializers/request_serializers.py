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
