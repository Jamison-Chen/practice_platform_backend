from django.urls import path, include

from rest_framework.authtoken import views as authviews

from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r"account", AccountViewSet, basename="account")

urlpatterns = [
    path("", include(router.urls)),
    path("create_tenant_user", views.create_tenant_user),
    path("get-auth-token", authviews.obtain_auth_token),
    path("list-all", views.list_tenant_user),
    path("upload-avatar", views.upload_avatar),
]
