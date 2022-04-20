# from django.conf import settings
from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate

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
            return JsonResponse(res)
        except Exception as e:
            res["status"] = "failed"
            try:
                res["error-message"] = str(list(e)[0])
            except:
                res["error-message"] = str(e)
            return HttpResponseNotFound(JsonResponse(res))
    else:
        res["status"] = "failed"
        res["error-message"] = "Please log in."
        return HttpResponseNotFound(JsonResponse(res))


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
            return HttpResponseNotFound(JsonResponse(res))
    else:
        res["error-message"] = "Info not sufficient."
        res["status"] = "failed"
        return HttpResponseNotFound(JsonResponse(res))
    """
    "status": string,
    "error-message": string,
    "user-info": dict
    """


@csrf_exempt
@require_POST
def checkLogin(request):
    """
    "fake-domain-name": string,
    """
    res = {"data": False, "username": "", "error-message": ""}
    try:
        if request.user:
            res["data"] = True
            res["username"] = request.user.username
    except Exception as e:
        res["error-message"] = str(e)
    return JsonResponse(res)
    """
    "data": boolean,
    "username": string
    """


@csrf_exempt
@require_POST
def logout(request):
    """
    "fake-from-domain": string
    """
    res = {"status": ""}
    Token.objects.filter(user=request.user).delete()
    res["status"] = "succeeded"
    res = JsonResponse(res)
    res.headers["is-log-out"] = "yes"
    res.delete_cookie("token", samesite="None")
    return res
    """
    "status": "succeeded" | "failed"
    """


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
            return JsonResponse(res)
        else:
            res["status"] = "failed"
            res["error-message"] = "Please log in."
            return HttpResponseNotFound(JsonResponse(res))
    except Exception as e:
        res["error-message"] = str(e)
        return HttpResponseNotFound(JsonResponse(res))


@csrf_exempt
@require_POST
def upload_avatar(request):
    res = {"status": "", "user-info": {}, "error-message": ""}
