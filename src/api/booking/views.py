from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import ujson as json
from booking.service_layer import services, unit_of_work
import uuid
from rest_framework import viewsets
from booking.serializers import ScreeningListSerializer, ScreeningSerializer
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
    return JsonResponse(
        {
            "success": True,
            "screening_id": data["screening_id"],
            "reservation_number": data["reservation_number"],
        },
        status=201,
    )


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

    return JsonResponse({"success": True}, status=200)


class ScreeningViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Screening.objects.all()

    def get_serializer_class(self):
        if self.action_map["get"] == "list":
            return ScreeningListSerializer
        return ScreeningSerializer
