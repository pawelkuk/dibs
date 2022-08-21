from celery import shared_task
from booking.domain import events


@shared_task
def screening_changed_notification(event: events.ScreeningChanged):
    print("request to read model service")
