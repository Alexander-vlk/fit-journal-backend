from django.db import models


class AutoDateMixin(models.Model):
    """Mixin для полей даты-времени создания и обновления записей"""

    dt_created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    dt_updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        abstract = True
