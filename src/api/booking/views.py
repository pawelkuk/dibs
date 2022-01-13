from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from booking.domain import model
from booking.service_layer import services, unit_of_work


@csrf_exempt
def make_reservation(request):
    try:
        services.make_reservation(
            customer_id=request.json["customer_id"],
            screening_id=request.json["screening_id"],
            reservation_number=request.json["reservation_number"],
            seats_data=request.json["seats_data"],
            uow=unit_of_work.DjangoUnitOfWork(),
        )
    except model.SeatsCollide as e:
        return {"message": str(e)}, 400
    return "OK", 201


@csrf_exempt
def cancel_reservation(request):
    try:
        services.cancel_reservation(
            reservation_number=request.json["customer_id"],
            screening_id=request.json["screening_id"],
            uow=unit_of_work.DjangoUnitOfWork(),
        )
    except model.ReservationDoesNotExists as e:
        return JsonResponse({"message": str(e)}, status=404)

    return JsonResponse({"success": "True"}, status=204)
