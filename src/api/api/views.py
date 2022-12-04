from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.serializers import DibsSerializer
import ujson as json
from api import tasks
from api.service_layer import services
from django.conf import settings


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
    try:
        services.dibs(
            **dibs_serializer.validated_data,
            payment_success_rate=settings.PAYMENT_SUCCESS_RATE,
            ticketing_success_rate=settings.TICKET_RENDER_SUCCESS_RATE
        )
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)
    return JsonResponse(..., status=200)