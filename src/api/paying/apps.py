from django.apps import AppConfig
from django.conf import settings


class PayingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "paying"

    def ready(self):
        if settings.SQL_ALCHEMY_ORM_ENABLED:

            from paying.adapters import orm

            orm.start_mappers()