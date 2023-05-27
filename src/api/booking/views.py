from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import ujson as json
from booking.service_layer import services
from api.service_layer import unit_of_work
from rest_framework.decorators import action
from rest_framework.response import Response

import uuid
from rest_framework import viewsets
from booking.serializers import ScreeningListSerializer, ScreeningSerializer
from booking import models
from django.conf import settings


@csrf_exempt
def make_reservation(request: HttpRequest):
    data = json.loads(request.body)
    try:
        services.make_reservation(
            customer_id=uuid.UUID(data["customer_id"]),
            screening_id=uuid.UUID(data["screening_id"]),
            reservation_number=uuid.UUID(data["reservation_number"]),
            seats_data=data["seats_data"],
            uow=unit_of_work.SqlAlchemyUnitOfWork(
                settings.SQL_ALCHEMY_ISOLATION_LEVEL, twophase=False
            ),
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
            uow=unit_of_work.SqlAlchemyUnitOfWork(
                settings.SQL_ALCHEMY_ISOLATION_LEVEL, twophase=False
            ),
        )
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)

    return JsonResponse({"success": True}, status=200)


class ScreeningViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Screening.objects.filter(is_full=False).prefetch_related(
        "reservations", "reservations__reservation_seats"
    )

    def get_serializer_class(self):
        if self.action_map["get"] == "list":
            return ScreeningListSerializer
        return ScreeningSerializer

    @action(
        detail=True,
        methods=["patch"],
        name="Mark screening as full. Will not be returned in list of screenings",
    )
    def mark_as_full(self, request, pk=None):
        screening = self.get_object()
        if screening.is_full:
            return Response({"msg": "Screening is already full"}, status=200)
        screening.is_full = True
        screening.save()
        return Response(status=200)

    @action(
        detail=False,
        methods=["post"],
        name="Create partially booked screening.",
    )
    def partially_booked(self, request):
        from booking.management.commands import initial_data

        try:
            cmd = initial_data.Command()
            cmd.handle()
            screening = cmd.screening
            return Response(
                {
                    "screening_id": screening.screening_id,
                    "movie": screening.movie.title,
                },
                status=200,
            )
        except Exception as e:
            return Response({"msg": str(e)}, status=400)
