from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.serializers import DibsSerializer
import ujson as json
from api import tasks
from api.service_layer import services
from django.conf import settings
from api.service_layer import unit_of_work


@csrf_exempt
def dibs(request: HttpRequest):
    data: dict = json.loads(request.body)
    dibs_serializer = DibsSerializer(data=data)
    if not dibs_serializer.is_valid():
        return JsonResponse({"errors": dibs_serializer.errors}, status=400)
    tasks.dibs(dibs_serializer.validated_data)
    return JsonResponse({"success": True}, status=200)


@csrf_exempt
def dibs_two_phase_commit(request: HttpRequest):
    data: dict = json.loads(request.body)
    dibs_serializer = DibsSerializer(data=data)
    if not dibs_serializer.is_valid():
        return JsonResponse({"errors": dibs_serializer.errors}, status=400)
    # try:
    res = services.dibs(
        **dibs_serializer.validated_data,
        payment_success_rate=settings.PAYMENT_SUCCESS_RATE,
        ticketing_success_rate=settings.TICKET_RENDER_SUCCESS_RATE,
        uow=unit_of_work.SqlAlchemyUnitOfWork(settings.SQL_ALCHEMY_ISOLATION_LEVEL)
    )
    # except Exception as e:
    # return JsonResponse({"message": str(e)}, status=400)
    return JsonResponse({"success": True}, status=200)
