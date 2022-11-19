from django.apps import AppConfig
from django.conf import settings


class TicketingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ticketing"

    def ready(self):
        if settings.SQL_ALCHEMY_ORM_ENABLED:

            from ticketing.adapters import orm

            orm.start_mappers()