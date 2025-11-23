import re

from django.db import models
from transliterate import translit

from auth_service.models import Athlete
from utils.mixins import AutoDateMixin


class Exercise(AutoDateMixin):
    """Справочник упражнений"""

    name = models.CharField(verbose_name='Название', max_length=200)
    translit = models.SlugField(
        verbose_name='Транслит',
        max_length=200,
        unique=True,
        help_text='Заполняется автоматически на основе названия',
    )
    available_for_user = models.BooleanField(verbose_name='Доступно для выбора пользователю', default=False)

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Справочник упражнений'
        ordering = ['name']

    def __str__(self):
        """Строковое представление объекта модели"""
        return f'Упражнение: {self.name}'

    def save(self, *args, **kwargs):
        """Перегрузить метод сохранения"""
        raw_translit = self.name.lower()
        raw_translit = translit(raw_translit, 'ru', reversed=True)
        raw_translit = re.sub(r'\s', '_', raw_translit)
        self.translit = re.sub(r'[^a-z0-9_]', '', raw_translit)
        super().save(*args, **kwargs)


class Training(AutoDateMixin):
    """Тренировка"""

    athlete = models.ForeignKey(Athlete, verbose_name='Спортсмен', on_delete=models.PROTECT, related_name='trainings')
    exercises = models.ManyToManyField(Exercise, verbose_name='Упражнения', related_name='trainings')
    date = models.DateField(verbose_name='Дата проведения', db_index=True)

    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'
        ordering = ['-date']

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
    comment = models.CharField(verbose_name='Комментарий', max_length=200, blank=True, default='')

    class Meta:
        verbose_name = 'Подход'
        verbose_name_plural = 'Подходы'

    def __str__(self):
        """Строковое представление объекта модели"""
        return f'{self.exercise.name}: {self.repetition} / {self.weight}'

    def save(self, *args, **kwargs):
        """Расширение метода сохранения"""
        if self.exercise not in self.training.exercises.all():
            self.training.exercises.add(self.exercise)
        super().save(*args, **kwargs)

    def delete(self, **kwargs):
        """Расширение метода удаления"""
        self.training.exercises.remove(self.exercise)
        super().delete(**kwargs)
