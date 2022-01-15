from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import ujson as json
from booking.domain import model
from booking.service_layer import services, unit_of_work


@csrf_exempt
def make_reservation(request):
    data = json.loads(request.body)
    try:
        services.make_reservation(
            customer_id=data["customer_id"],
            screening_id=data["screening_id"],
            reservation_number=data["reservation_number"],
            seats_data=data["seats_data"],
            uow=unit_of_work.DjangoUnitOfWork(),
        )
    except model.SeatsCollide as e:
        return JsonResponse({"message": str(e)}, status=400)
    return JsonResponse({"success": "True"}, status=201)


@csrf_exempt
def cancel_reservation(request):
    data = json.loads(request.body)
    try:
        services.cancel_reservation(
            reservation_number=data["customer_id"],
            screening_id=data["screening_id"],
            uow=unit_of_work.DjangoUnitOfWork(),
        )
    except model.ReservationDoesNotExists as e:
        return JsonResponse({"message": str(e)}, status=404)

    return JsonResponse({"success": "True"}, status=204)
