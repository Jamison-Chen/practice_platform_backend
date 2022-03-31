# from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# from rest_framework import viewsets
# from django.http import HttpResponse, JsonResponse
# from rest_framework.decorators import action

from .models import user
from .utils import validate_account_info

# from .serializers import AccountSerializer


@csrf_exempt
@require_POST
def create_tenant_user(request):
    res = {"data": {"status": None}}
    try:
        validate_account_info(request)
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        ############## This part is for testing only. ##########################
        ############## For the reason that we don't actually use ###############
        ############## dedicatede domain as the host name at the frontend. #####
        from django.db import connection
        from ..core.utils import get_tenant_schema_name

        with connection.cursor() as cursor:
            schemaName = get_tenant_schema_name(request.POST.get("fake-from-domain"))
            if not schemaName:
                raise Exception("This domain doesn't have a dedicated schema.")
            cursor.execute("SET search_path to {};".format(schemaName))
        ########################################################################

        user.objects.create_tenant_user(email, password, username=username)
        res["data"]["status"] = "succeeded"
    except Exception as e:
        res["data"]["status"] = "failed"
        res["data"]["error-message"] = str(e)
    return JsonResponse(res)


@csrf_exempt
@require_POST
def list_tenant_user(request):
    res = {"data": []}
    if request.user.is_authenticated:
        ############## This part is for testing only. ##########################
        ############## For the reason that we don't actually use ###############
        ############## dedicatede domain as the host name at the frontend. #####
        from django.db import connection
        from ..core.utils import get_tenant_schema_name

        with connection.cursor() as cursor:
            schemaName = get_tenant_schema_name(request.POST.get("fake-from-domain"))
            if not schemaName:
                raise Exception("This domain doesn't have a dedicated schema.")
            cursor.execute("SET search_path to {};".format(schemaName))
        ########################################################################

        for each in user.objects.all_staff():
            res["data"].append({"username": each.username})
    else:
        res["error-message"] = "Please log in."

    return JsonResponse(res)


@csrf_exempt
@require_POST
def upload_avatar(request):
    res = {"data": []}
