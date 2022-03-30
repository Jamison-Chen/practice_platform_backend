from django.urls import path, include
from . import views

urlpatterns = [path("create", views.create), path("remove", views.remove)]
