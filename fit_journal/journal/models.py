from django.db import models
from transliterate import translit

from auth_service.models import Athlete
from utils.mixins import AutoDateMixin


class Exercise(AutoDateMixin):
    """Справочник упражнений"""

    name = models.CharField(verbose_name='Название', max_length=200)
    translit = models.SlugField(verbose_name='Транслит', max_length=200, blank=True, default='')

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Справочник упражнений'
        ordering = ['name']

    def __str__(self):
        """Строковое представление объекта модели"""
        return f'Упражнение: {self.name}'

    def save(self, *args, **kwargs):
        """Перегрузить метод сохранения"""
        self.slug = translit(self.name)
        super().save(*args, **kwargs)


class Training(AutoDateMixin):
    """Тренировка"""

    athlete = models.ForeignKey(Athlete, verbose_name='Спортсмен', on_delete=models.PROTECT, related_name='trainings')
    exercises = models.ManyToManyField(Exercise, verbose_name='Упражнения', related_name='trainings')
    date = models.DateField(verbose_name='Дата проведения', db_index=True)

    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'
        ordering = ['date']

    def __str__(self):
        """Строковое представление объекта модели"""
        return f'{self.athlete_id}: {self.date}'


class ExerciseSet(AutoDateMixin):
    """Подход"""

    exercise = models.ForeignKey(
        Exercise,
        verbose_name='Упражнение',
        on_delete=models.PROTECT,
        related_name='sets',
    )
    training = models.ForeignKey(
        Training,
        verbose_name='Тренировка',
        on_delete=models.PROTECT,
        related_name='sets',
    )
    repetition = models.PositiveSmallIntegerField(verbose_name='Число повторений')
    weight = models.PositiveSmallIntegerField(verbose_name='Вес')
    comment = models.CharField(verbose_name='Комментарий', max_length=200)

    class Meta:
        verbose_name = 'Подход'
        verbose_name_plural = 'Подходы'

    def __str__(self):
        """Строковое представление объекта модели"""
        return f'{self.exercise.name}: {self.repetition} / {self.weight}'
