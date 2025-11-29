from django.contrib import admin

from journal.models import Exercise, ExerciseSet, Training, Color, TrainingType, AthleteTrainingTypeColor


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    """Админ для Color"""

    list_display = ['id', 'background_color', 'text_color']


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """Админ для Exercise"""

    list_display = ['name', 'translit', 'available_for_user']
    readonly_fields = ['translit']


@admin.register(ExerciseSet)
class ExerciseSetAdmin(admin.ModelAdmin):
    """Админ для ExerciseSet"""

    list_display = ['exercise', 'training', 'repetition', 'weight']
    raw_id_fields = ['exercise', 'training']


@admin.register(TrainingType)
class TrainingTypeAdmin(admin.ModelAdmin):
    """Админ для TrainingType"""

    list_display = ['name']


@admin.register(AthleteTrainingTypeColor)
class AthleteTrainingTypeColorAdmin(admin.ModelAdmin):
    """Админ для AthleteTrainingTypeColor"""

    list_display = ['id', 'athlete', 'training_type', 'color']
    raw_id_fields =['athlete', 'training_type', 'color']


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    """Админ для Training"""

    list_display = ['athlete', 'date']
    raw_id_fields = ['athlete']
