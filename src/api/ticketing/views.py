from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import ujson as json
from ticketing.domain import model
from ticketing.service_layer import services
from api.service_layer import unit_of_work

import uuid
from django.conf import settings


@csrf_exempt
def render_ticket(request: HttpRequest):
    data = json.loads(request.body)
    try:
        ticket_id = services.render_ticket(
            details=data["details"],
            reservation_id=uuid.UUID(data["reservation_id"]),
            uow=unit_of_work.SqlAlchemyUnitOfWork(
                settings.SQL_ALCHEMY_ISOLATION_LEVEL, twophase=False
            ),
            success_rate=settings.TICKET_RENDER_SUCCESS_RATE,
        )
    except model.TicketRenderError as e:
        return JsonResponse({"message": str(e)}, status=400)
    return JsonResponse({"success": True, "ticket_id": ticket_id}, status=201)
