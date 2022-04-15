from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .utils import (
    validate_domain_name,
    create_tenant_schema,
    read_tenant_info,
    update_tenant_info,
    remove_multiple_tenant_schema,
    list_all_tenants,
)


@csrf_exempt
@require_POST
def check(request):
    """
    domain-name: string,
    """
    res = {"data": None, "error-message": ""}
    try:
        validate_domain_name(request)
        res["data"] = True
    except Exception as e:
        res["data"] = False
        res["error-message"] = str(e)
    return JsonResponse(res)
    """
    "data": boolean,
    "error-message": string,
    """


@csrf_exempt
@require_POST
def create(request):
    """
    domain-name: string,
    username: string,
    email: string,
    password: string,
    """
    res = {"status": "", "domain": "", "error-message": ""}
    try:
        result = create_tenant_schema(request)
        res["status"] = "succeeded"
        res["domain"] = result["domain-name"]
    except Exception as e:
        res["status"] = "failed"
        res["error-message"] = str(e)
    return JsonResponse(res)
    """
    "status": string,
    "domain": string,
    "error-message": string,
    """


@csrf_exempt
@require_POST
def read(request):
    """
    fake-domain-name: string
    """
    res = {
        "status": "",
        "is-login": False,
        "username": "",
        "error-message": "",
        "data": {},
    }
    if request.user:
        try:
            res["is-login"] = True
            res["username"] = request.user.username
            res["data"] = read_tenant_info(request)
            res["status"] = "succeeded"
        except Exception as e:
            res["error-message"] = str(e)
            res["status"] = "failed"
    else:
        res["status"] = "failed"
        res["error-message"] = "Please log in."
    return JsonResponse(res)
    """
    "status": string,
    "is-login": boolean,
    "error-message": string,
    "data":{
        "brand-name": string,
        "tax-id-number": string,
        "logo": string,
        "tel": string,
    }
    """


@csrf_exempt
@require_POST
def update(request):
    """
    fake-domain-name: string,
    brand-name: string,
    tax-id-number: string,
    logo: string,
    tel: string
    """
    res = {"status": "", "is-login": False, "error-message": "", "data": {}}
    if request.user:
        res["is-login"] = True
        res["data"] = update_tenant_info(request)
        res["status"] = "succeeded"
    else:
        res["status"] = "failed"
        res["error-message"] = "Please log in."
    return JsonResponse(res)
    """
    "brand-name": string,
    "tax-id-number": string,
    "logo": string,
    "tel": string,
    """


###### This function is only for testing. ########
@csrf_exempt
@require_POST
def delete(request):
    res = {"status": "", "error-message": ""}
    try:
        remove_multiple_tenant_schema(request)
        res["status"] = "succeeded"
    except Exception as e:
        res["error-message"] = str(e)
        res["status"] = "failed"
    return JsonResponse(res)
    """
    "status": string,
    "error-message": string,
    """


#################################################


@csrf_exempt
@require_POST
def list(request):
    res = {"status": "", "data": [], "error-message": ""}
    try:
        res["data"] = list_all_tenants()
        res["status"] = "succeeded"
    except Exception as e:
        res["error-message"] = str(e)
        res["status"] = "failed"
    return JsonResponse(res)
