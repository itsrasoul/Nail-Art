from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    def ready(self):
        # import signals to ensure profile/cart creation on user create
        import store.signals  # noqa
from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "store"
