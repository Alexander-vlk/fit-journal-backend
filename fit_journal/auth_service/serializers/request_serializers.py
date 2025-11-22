from django.contrib.auth.password_validation import validate_password
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers


@extend_schema_serializer(
    many=False,
    examples=[
        OpenApiExample(
            'Стандартный ответ',
            value={
                'old_password': 'test',
                'new_password': 'test1',
                'new_password2': 'test1',
            },
        ),
    ],
)
class ChangePasswordRequestSerializer(serializers.Serializer):
    """Сериализатор ответа для смены пароля"""

    old_password = serializers.CharField(help_text='Старый пароль')
    new_password = serializers.CharField(help_text='Новый пароль')
    new_password2 = serializers.CharField(help_text='Новый пароль (еще раз)')

    def validate_old_password(self, old_password_value):
        """Проверить, что старый пароль введен верно"""
        if not self.context['user'].check_password(old_password_value):
            raise serializers.ValidationError('Старый пароль неверный')

        return old_password_value

    def validate_new_password(self, new_password_value):
        """Проверить новый пароль"""
        validate_password(new_password_value, user=self.context['user'])
        return new_password_value

    def validate(self, obj):
        """Проверка"""
        if obj['old_password'] == obj['new_password']:
            raise serializers.ValidationError('Новый пароль совпадает со старым')
        if obj['new_password'] != obj['new_password2']:
            raise serializers.ValidationError('Пароли не совпадают')

        return obj