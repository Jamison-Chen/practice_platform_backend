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

# from .serializers import AccountSerializer


@csrf_exempt
@require_POST
def create_tenant_user(request):
    res = {
        "login-status": "login" if request.user else "logout",
        "user-info": None,
        "status": None,
    }
    if request.user:
        res["user-info"] = request.user.username
        try:
            validate_account_info(request)
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            User.objects.create_tenant_user(email, password, username=username)
            res["status"] = "succeeded"
        except Exception as e:
            res["status"] = "failed"
            res["error-message"] = str(e)
    return JsonResponse(res)


@csrf_exempt
@require_POST
def login(request):
    res = {
        "login-status": "unknown",
        "user-info": None,
    }
    if (email := request.POST.get("email")) and (
        password := request.POST.get("password")
    ):
        try:
            user = authenticate(request, email=email, password=password)
            res["user-info"] = user.username
            token = Token.objects.get_or_create(user=user)[0].key
            res["login-status"] = "login"
            res = JsonResponse(res)
            res.headers["new-token"] = token
            return res
        except Exception as e:
            return JsonResponse({"login-status": str(e)})
    else:
        return JsonResponse(res)


@csrf_exempt
@require_POST
def logout(request):
    res = {"login-status": "login" if request.user else "logout"}
    Token.objects.filter(user=request.user).delete()
    res = JsonResponse(res)
    res.headers["is-log-out"] = "yes"
    res.delete_cookie("token", samesite="None")
    return res


@csrf_exempt
@require_POST
def list_tenant_user(request):
    res = {
        "login-status": "logout",
        "data": [],
        "user-info": None,
    }
    if request.user:
        res["user-info"] = request.user.username
        res["login-status"] = "login"
        for each in User.objects.all_staff():
            res["data"].append({"username": each.username})

    return JsonResponse(res)


@csrf_exempt
@require_POST
def upload_avatar(request):
    res = {
        "status": None,
        "user-info": None,
    }
