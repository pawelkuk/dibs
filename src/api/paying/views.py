from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import ujson as json
from paying.domain import model
from paying.service_layer import services, unit_of_work
import uuid


@csrf_exempt
def pay(request):
    data = json.loads(request.body)
    try:
        payment_id = services.pay(
            amount=data["amount"],
            currency=data["currency"],
            user_id=uuid.UUID(data["user_id"]),
            uow=unit_of_work.DjangoUnitOfWork(),
        )
    except model.PaymentError as e:
        return JsonResponse({"message": str(e)}, status=400)
    return JsonResponse({"success": True, "payment_id": payment_id}, status=201)


@csrf_exempt
def refund(request):
    data = json.loads(request.body)
    try:
        services.refund(
            amount=data["payment_id"],
            uow=unit_of_work.DjangoUnitOfWork(),
        )
    except model.PaymentError as e:
        return JsonResponse({"message": str(e)}, status=400)
    return JsonResponse({"success": True}, status=204)
