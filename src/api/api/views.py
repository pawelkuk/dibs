from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import ujson as json
from api.tasks import dibs

@csrf_exempt    
def dibs(request: HttpRequest):
    data: dict = json.loads(request.body)
    try:
        dibs.delay(**data)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)
    return JsonResponse({"success": True}, status=200)
