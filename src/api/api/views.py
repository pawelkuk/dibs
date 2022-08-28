from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.serializers import DibsSerializer
import ujson as json
from api import tasks


@csrf_exempt
def dibs(request: HttpRequest):
    data: dict = json.loads(request.body)
    dibs_serializer = DibsSerializer(data=data)
    if not dibs_serializer.is_valid():
        return JsonResponse({"errors": dibs_serializer.errors}, status=400)
    tasks.dibs(dibs_serializer.validated_data)
    return JsonResponse({"success": True}, status=200)
