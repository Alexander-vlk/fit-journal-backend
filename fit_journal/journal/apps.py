from django.apps import AppConfig


class JournalConfig(AppConfig):
    """Конфиг приложения journal"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'journal'
    verbose_name = 'Журнал тренировок'

    def ready(self):
        """Подготовка сигналов"""
        import journal.signals
