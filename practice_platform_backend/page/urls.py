from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

urlpatterns = [
    path("create", views.create_article),
    path("read", views.read_article),
    path("update", views.update_article),
]
