from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.mixins import AutoDateMixin


class Athlete(AbstractUser, AutoDateMixin):
    """Спортсмен"""

    second_name = models.CharField(verbose_name='Отчество', max_length=60, blank=True, default='')
    phone = models.CharField(verbose_name='Номер телефона', max_length=13, blank=True, default='')

    class Meta:
        verbose_name = 'Спортсмен'
        verbose_name_plural = 'Спортсмены'
        indexes = (
            models.Index(fields=('dt_created',), name='athlete_dt_created_idx'),
        )
        ordering = ['-dt_created']

    def __str__(self):
        """Строковое представление объекта модели"""
        return f'{self.username}: {self.last_name} {self.first_name}'
