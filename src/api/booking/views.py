from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import ujson as json
from booking.service_layer import services, unit_of_work
import uuid
from rest_framework import viewsets
from booking.serializers import ScreeningModelSerializer
from booking import models


@csrf_exempt
def make_reservation(request: HttpRequest):
    data = json.loads(request.body)
    try:
        services.make_reservation(
            customer_id=uuid.UUID(data["customer_id"]),
            screening_id=uuid.UUID(data["screening_id"]),
            reservation_number=uuid.UUID(data["reservation_number"]),
            seats_data=data["seats_data"],
            uow=unit_of_work.DjangoUnitOfWork(),
        )
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)
    return JsonResponse({"success": True}, status=201)


@csrf_exempt
def cancel_reservation(request: HttpRequest):
    data = json.loads(request.body)
    try:
        services.cancel_reservation(
            reservation_number=uuid.UUID(data["reservation_number"]),
            screening_id=uuid.UUID(data["screening_id"]),
            uow=unit_of_work.DjangoUnitOfWork(),
        )
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)

    return JsonResponse({"success": True}, status=204)


class ScreeningViewSet(viewsets.ModelViewSet):
    serializer_class = ScreeningModelSerializer
    queryset = models.Screening.objects.all()
