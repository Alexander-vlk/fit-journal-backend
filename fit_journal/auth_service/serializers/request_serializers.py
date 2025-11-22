from cfgv import ValidationError
from django.contrib.auth.password_validation import validate_password as django_validate_password
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from auth_service.models import Athlete


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
        django_validate_password(new_password_value, user=self.context['user'])
        return new_password_value

    def validate(self, obj):
        """Проверка"""
        if obj['old_password'] == obj['new_password']:
            raise serializers.ValidationError('Новый пароль совпадает со старым')
        if obj['new_password'] != obj['new_password2']:
            raise serializers.ValidationError('Пароли не совпадают')

        return obj


@extend_schema_serializer(
    many=False,
    examples=[
        OpenApiExample(
            'Стандартный запрос',
            value={
                'username': 'username',
                'email': 'email',
                'last_name': 'last_name',
                'first_name': 'first_name',
                'second_name': 'second_name',
                'phone': 'phone'
            },
        ),
    ],
)
class AthleteRequestSerializer(serializers.ModelSerializer):
    """Сериализатор модели Athlete"""

    class Meta:
        model = Athlete
        fields = [
            'username',
            'email',
            'last_name',
            'first_name',
            'second_name',
            'phone',
        ]


@extend_schema_serializer(
    many=False,
    examples=[
        OpenApiExample(
            'Стандартный запрос',
            value={
                'username': 'username',
                'email': 'email',
                'last_name': 'last_name',
                'first_name': 'first_name',
                'second_name': 'second_name',
                'phone': 'phone',
                'password': 'password',
                'password2': 'password2',
            },
        ),
    ],
)
class RegisterAthleteRequestSerializer(serializers.Serializer):
    """Сериализатор запроса модели Athlete"""

    username = serializers.CharField(help_text='Имя пользователя', max_length=150)
    email = serializers.EmailField(help_text='Электронная почта', allow_blank=True)
    last_name = serializers.CharField(help_text='Фамилия', allow_blank=True, max_length=60)
    first_name = serializers.CharField(help_text='Имя', allow_blank=True, max_length=60)
    second_name = serializers.CharField(help_text='Отчество', allow_blank=True, max_length=60)
    phone = serializers.CharField(help_text='Номер телефона', allow_blank=True, max_length=13)

    password = serializers.CharField(help_text='Пароль', max_length=128)
    password2 = serializers.CharField(help_text='Пароль (еще раз)', max_length=128)

    def validate_username(self, username):
        """Проверить имя пользователя"""
        if Athlete.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует')

        return username

    def validate_password(self, password):
        """Проверить пароль"""
        django_validate_password(password)
        return password

    def validate(self, obj):
        """Проверка"""
        if obj['password'] != obj['password2']:
            raise serializers.ValidationError('Пароли не совпадают')

        return obj
