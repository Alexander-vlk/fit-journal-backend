from django.contrib import admin

from journal.models import Exercise, ExerciseSet, Training


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """Админ для Exercise"""

    list_display = ['name', 'translit']
    readonly_fields = ['translit']


@admin.register(ExerciseSet)
class ExerciseSetAdmin(admin.ModelAdmin):
    """Админ для ExerciseSet"""

    list_display = ['exercise', 'training', 'repetition', 'weight']
    raw_id_fields = ['exercise', 'training']


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    """Админ для Training"""

    list_display = ['athlete', 'date']
    raw_id_fields = ['athlete']
