from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import ujson as json
from paying.domain import model
from paying import models
from paying.service_layer import services
from api.service_layer import unit_of_work
from rest_framework import viewsets
from paying import serializers


import uuid
from django.conf import settings


@csrf_exempt
def pay(request: HttpRequest):
    data = json.loads(request.body)
    try:
        payment_id = services.pay(
            amount=data["amount"],
            currency=model.Currency[data["currency"]],
            user_id=uuid.UUID(data["user_id"]),
            uow=unit_of_work.SqlAlchemyUnitOfWork(
                settings.SQL_ALCHEMY_ISOLATION_LEVEL, twophase=False
            ),
            payment_success_rate=settings.PAYMENT_SUCCESS_RATE,
        )
    except model.PaymentError as e:
        return JsonResponse({"message": str(e)}, status=400)
    return JsonResponse({"success": True, "payment_id": payment_id}, status=201)


@csrf_exempt
def refund(request: HttpRequest):
    data = json.loads(request.body)
    try:
        services.refund(
            payment_id=data["payment_id"],
            uow=unit_of_work.SqlAlchemyUnitOfWork(
                settings.SQL_ALCHEMY_ISOLATION_LEVEL, twophase=False
            ),
        )
    except model.PaymentError as e:
        return JsonResponse({"message": str(e)}, status=400)
    return JsonResponse({"success": True}, status=200)


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer