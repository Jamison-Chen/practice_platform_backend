from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path(r"admin/", admin.site.urls),
    path(r"api/shop/", include("practice_platform_backend.core.urls")),
    path(r"api/account/", include("practice_platform_backend.account.urls")),
    path(r"api/article/", include("practice_platform_backend.page.urls")),
    path(r"tests/", include("practice_platform_backend.tests.urls")),
    # api-auth/login is the login page provided by REST framework
    path(r"api-auth/", include("rest_framework.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
