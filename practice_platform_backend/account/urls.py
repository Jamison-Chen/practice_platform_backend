from django.urls import path, include

from . import views

# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r"account", AccountViewSet, basename="account")
# urlpatterns = router.urls

urlpatterns = [
    path("create", views.create_tenant_user),
    path("list-all", views.list_tenant_user),
    path("upload-avatar", views.upload_avatar),
]
