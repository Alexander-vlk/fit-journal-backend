import re

from django.core.validators import RegexValidator
from django.db import models
from transliterate import translit

from auth_service.models import Athlete
from utils.mixins import AutoDateMixin


class Color(AutoDateMixin):
    """Цвет"""

    background_color = models.CharField(
        verbose_name='Цвет фона',
        help_text='TailwindCSS-стиль',
        validators=[RegexValidator(regex=r'^bg-[a-z]+-\d+$')],
        max_length=30,
    )
    text_color = models.CharField(
        verbose_name='Цвет текста',
        help_text='TailwindCSS-стиль',
        validators=[RegexValidator(regex=r'^text-[a-z]+-\d+$')],
        max_length=30,
    )

    class Meta:
        verbose_name = 'Цветовая схема'
        verbose_name_plural = 'Справочник цветовых схем'
        unique_together = (('background_color', 'text_color'),)

    def __str__(self):
        return f'{self.background_color} {self.text_color}'


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


class TrainingType(AutoDateMixin):
    """Тип тренировки"""

    name = models.CharField(verbose_name='Название', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Тип тренировки'
        verbose_name_plural = 'Справочник типов тренировок'
        ordering = ['name']

    def __str__(self):
        """Строковое представление объекта модели"""
        return self.name


class AthleteTrainingTypeColor(AutoDateMixin):
    """Связка цвет - тип тренировки для пользователя"""

    athlete = models.ForeignKey(Athlete, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    training_type = models.ForeignKey(TrainingType, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Связка Спортсмен - Цвет - Тип тренировки'
        verbose_name_plural = 'Связки Спортсмен - Цвет - Тип тренировки'

    def __str__(self):
        """Строковое представление объекта модели"""
        return f'{self.athlete} - {self.color} - {self.training_type}'


class Training(AutoDateMixin):
    """Тренировка"""

    athlete = models.ForeignKey(Athlete, verbose_name='Спортсмен', on_delete=models.PROTECT, related_name='trainings')
    athlete_training_type = models.ForeignKey(
        AthleteTrainingTypeColor,
        on_delete=models.PROTECT,
        related_name='trainings',
        null=True,
        blank=True,
    )
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
