from django.contrib.auth import authenticate
from django.conf import settings

from rest_framework.authtoken.models import Token

from .utils import connect_to_tenant_schema, fake_connect_to_tenant_schema


def tenant_identification_middleware(get_response):
    def middleware(request):
        # Code to be executed for each request before the view and later middleware are called.
        connect_to_tenant_schema(request)
        #

        response = get_response(request)

        # Code to be executed for each request/response after the view is called.
        # ...
        #
        return response

    return middleware


def fake_tenant_identification_middleware(get_response):
    def middleware(request):
        # Code to be executed for each request before the view and later middleware are called.
        if request.path == "/api/create-shop/create":
            connect_to_tenant_schema(request)
        else:
            fake_connect_to_tenant_schema(request)
        #

        response = get_response(request)

        # Code to be executed for each request/response after the view is called.
        # ...
        #
        return response

    return middleware


def check_login_status_middleware(get_response):
    def middleware(request):
        token = None
        if user := authenticate(request, token=request.COOKIES.get("token")):
            token = request.COOKIES.get("token")
        request.user = user

        response = get_response(request)

        token = token or response.get("new-token")
        if (not (response.get("is-log-out") == "yes")) and token:
            response.set_cookie(
                "token",
                token,
                max_age=settings.CSRF_COOKIE_AGE,
                samesite=settings.CSRF_COOKIE_SAMESITE,
                secure=settings.CSRF_COOKIE_SECURE,
            )
        else:
            del response.headers["is-log-out"]
            del response.headers["new-token"]
        return response

    return middleware
