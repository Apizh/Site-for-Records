from django.apps import AppConfig


class RecordsConfig(AppConfig):
    verbose_name = "Для работы с постами"
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'records'

class CategoriesConfig(AppConfig):
    verbose_name = "Категории"
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'categories'