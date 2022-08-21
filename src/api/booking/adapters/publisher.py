from typing import Callable, Type
from booking.domain import events
from booking.tasks import screening_changed_notification


class CeleryPublisher:
    def publish(self, event: events.Event):
        for task in TASKS[type(event)]:
            task.delay(event)


TASKS: dict[Type[events.Event], list[Callable]] = {
    events.ScreeningChanged: [screening_changed_notification],
}
