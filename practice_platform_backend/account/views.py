# from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# from rest_framework import viewsets
# from django.http import HttpResponse, JsonResponse
# from rest_framework.decorators import action

from .models import user

# from .serializers import AccountSerializer


@csrf_exempt
@require_POST
def create_tenant_user(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    if username and email and password:
        user.objects.create_tenant_user(email, password, username=username)
    else:
        raise Exception("Please complete the form.")
