from django.apps import AppConfig
from django.conf import settings


class BookingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "booking"

    def ready(self):
        if settings.SQL_ALCHEMY_ORM_ENABLED:
            from booking.adapters import orm

            orm.start_mappers()