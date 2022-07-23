from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import ujson as json
from ticketing.domain import model
from ticketing.service_layer import services, unit_of_work
import uuid


@csrf_exempt
def render_ticket(request):
    data = json.loads(request.body)
    try:
        ticket_id = services.render_ticket(
            details=data["details"],
            reservation_id=uuid.UUID(data["reservation_id"]),
            uow=unit_of_work.DjangoUnitOfWork(),
        )
    except model.TicketRenderError as e:
        return JsonResponse({"message": str(e)}, status=400)
    return JsonResponse({"success": True, "ticket_id": ticket_id}, status=201)
