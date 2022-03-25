from django.urls import path, include
from .views import CarViewSet, index

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"car", CarViewSet, basename="car")
urlpatterns = router.urls

# urlpatterns = [path("test", index)]
