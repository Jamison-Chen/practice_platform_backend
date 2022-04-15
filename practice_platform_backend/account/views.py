# from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate

# from rest_framework import viewsets
# from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

from .models import user as User
from .utils import validate_account_info

from .serializers import AccountSerializer


@csrf_exempt
@require_POST
def create_tenant_user(request):
    res = {"status": "", "is-login": False, "user-info": {}, "error-message": ""}
    if request.user:  # require a login user
        try:
            validate_account_info(request)
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            User.objects.create_tenant_user(email, password, username=username)
            res["status"] = "succeeded"
            res["is-login"] = True
            res["user-info"]["username"] = request.user.username
        except Exception as e:
            res["status"] = "failed"
            res["error-message"] = str(e)
    else:
        res["status"] = "failed"
        res["error-message"] = "Please log in."
    return JsonResponse(res)


@csrf_exempt
@require_POST
def login(request):
    """
    "fake-from-domain": string,
    "email": string,
    "password": string
    """
    res = {"status": "", "error-message": "", "user-info": {}}
    if (email := request.POST.get("email")) and (
        password := request.POST.get("password")
    ):
        try:
            user = authenticate(request, email=email, password=password)
            res["user-info"]["username"] = user.username
            token = Token.objects.get_or_create(user=user)[0].key
            res["status"] = "succeeded"
            res = JsonResponse(res)
            res.headers["new-token"] = token
            return res
        except Exception as e:
            res["status"] = "failed"
            res["error-message"] = str(e)
            return JsonResponse(res)
    else:
        res["status"] = "failed"
        return JsonResponse(res)
    """
    "status": string,
    "error-message": string,
    "user-info": dict
    """


@csrf_exempt
@require_POST
def logout(request):
    res = {"status": ""}
    Token.objects.filter(user=request.user).delete()
    res = JsonResponse(res)
    res.headers["is-log-out"] = "yes"
    res.delete_cookie("token", samesite="None")
    res["status"] = "succeeded"
    return res


@csrf_exempt
@require_POST
def list_tenant_users(request):
    res = {
        "status": "",
        "is-login": False,
        "data": [],
        "user-info": {},
        "error-message": "",
    }
    try:
        if request.user:
            res["status"] = "succeeded"
            res["is-login"] = True
            res["user-info"]["username"] = request.user.username
            for each in User.objects.all_staff():
                res["data"].append({"username": each.username})
            # queryset = User.objects.all_staff()
            # serializer_class = AccountSerializer
            # res["data"] = serializer_class(queryset, many=True).data
        else:
            res["status"] = "failed"
            res["error-message"] = "Please log in."
    except Exception as e:
        res["error-message"] = str(e)
    return JsonResponse(res)


@csrf_exempt
@require_POST
def upload_avatar(request):
    res = {"status": "", "user-info": {}, "error-message": ""}
