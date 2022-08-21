from booking.serializers import ScreeningSerializer
from celery import shared_task
from booking.domain import events
from booking import models
import requests


@shared_task
def screening_changed_notification(event: events.ScreeningChanged):
    print("request to read model service")
    screening: models.Screening = models.Screening.objects.get(
        screening_id=event.screening_id
    )
    screening_data = ScreeningSerializer().to_representation(screening)
    response = requests.post("http://read_model:3001/update", json=screening_data)
    if response.status_code != 200:
        print(response.json())
