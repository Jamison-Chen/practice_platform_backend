from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .utils import create_tenant_schema, remove_multiple_tenant_schema
from ..account.utils import validate_account_info


@csrf_exempt
@require_POST
def create_tenant(request):
    res = {"data": None}
    try:
        # Validate the (admin) user info before creating the schema
        validate_account_info(request)
        createResult = create_tenant_schema(request)
        res["data"] = {"status": "succeeded", "domain": createResult["domain_name"]}
    except Exception as e:
        res["data"] = {"error-message": str(e)}
    return JsonResponse(res)


# This function is only for testing.
@csrf_exempt
@require_POST
def remove(request):
    res = {"data": None}
    try:
        remove_multiple_tenant_schema(request)
        res["data"] = {"status": "succeeded"}
    except Exception as e:
        res["data"] = {"status": "failed"}
    return JsonResponse(res)
