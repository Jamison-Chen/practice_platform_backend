from django.urls import path, include
from . import views

urlpatterns = [
    path("check-domain-available", views.check),
    path("create", views.create),
    path("read", views.read),
    path("update", views.update),
    path("delete", views.delete),
]
