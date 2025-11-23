from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from journal.models import Training, ExerciseSet


@receiver(m2m_changed, sender=Training.exercises.through)
def handle_exercises_changes(sender, instance, action, **kwargs):
    """Обновить связи подходов и упражнений"""
    if action not in ('post_add', 'post_remove', 'post_clear'):
        return

    exercise_ids_in_training = instance.exercises.values_list('id', flat=True)
    ExerciseSet.objects.filter(training=instance).exclude(exercise_id__in=exercise_ids_in_training).delete()
