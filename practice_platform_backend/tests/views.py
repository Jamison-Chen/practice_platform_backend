from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.decorators import action

from .models import car
from .serializers import CarSerializer


@csrf_exempt
def index(request):
    res = {
        "request.headers.get('Host')": request.headers.get("Host"),
        "request.get_host()": request.get_host(),
    }
    return JsonResponse(res)


class CarViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    @csrf_exempt
    def all(self, request):
        print(
            request.user,
            request.user.is_authenticated,
            request.get_host(),
            request.path_info,
        )
        res = {"data": None}
        if request.user.is_authenticated:
            queryset = car.objects.all()
            serializer_class = CarSerializer
            res["data"] = serializer_class(queryset, many=True).data
        else:
            res["data"] = "Please log in."
        return JsonResponse(res)
