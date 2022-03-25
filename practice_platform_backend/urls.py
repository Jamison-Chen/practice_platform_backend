from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(r"admin/", admin.site.urls),
    path(r"create-shop/", include("practice_platform_backend.core.urls")),
    path(r"api/account/", include("practice_platform_backend.account.urls")),
    path(r"tests/", include("practice_platform_backend.tests.urls")),
    # api-auth/login is the login page provided by REST framework
    path(r"api-auth/", include("rest_framework.urls")),
]
