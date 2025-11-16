from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auth_service.models import Athlete

@admin.register(Athlete)
class AthleteAdmin(UserAdmin):
    """Админ для модели Athlete"""

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            'Personal info',
            {
                'fields': (
                    'last_name',
                    'first_name',
                    'second_name',
                    'phone',
                    'email',
                ),
             },
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
