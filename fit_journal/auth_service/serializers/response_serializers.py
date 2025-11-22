from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from rest_framework.serializers import Serializer


@extend_schema_serializer(
    many=False,
    examples=[
        OpenApiExample(
            'Пример токена',
            value={
                'access_token': 'some_cool_key',
            },
        ),
    ],
)
class AccessTokenResponseSerializer(Serializer):
    """Сериализатор ответа хука CustomTokenObtainPair"""

    access_token = serializers.CharField(help_text='access_token', max_length=1000)
