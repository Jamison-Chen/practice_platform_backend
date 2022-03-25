from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .utils import create_tenant_schema
from ..account.utils import validate_account_info


@csrf_exempt
@require_POST
def create(request):
    res = {"data": None}
    try:
        validate_account_info(request)
        create_tenant_schema(request)
        res["data"] = "success"
    except Exception as e:
        res["data"] = str(e)
    return JsonResponse(res)
