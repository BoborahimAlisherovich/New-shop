from django.apps import AppConfig


class FruitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fruit'

    def ready(self):
        import fruit.signals
