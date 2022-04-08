from django.urls import path, include
from .views import index, all

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r"car", CarViewSet, basename="car")

urlpatterns = [
    path("", include(router.urls)),
    path("index", index),
    path("allcar", all),
]
