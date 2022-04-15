from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import car
from .serializers import CarSerializer


@csrf_exempt
def index(request):
    res = {
        "request.headers.get('Host')": request.headers.get("Host"),
        "request.get_host()": request.get_host(),
    }
    return JsonResponse(res)


@csrf_exempt
@api_view(["GET"])
def all_need_auth(request):
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


@csrf_exempt
def all(request):
    print(
        "---------------------------------\
        \nUser: {}\
        \nHost: {}\
        \nAPI Path: {}\
        \nFake From Domain: {}\
        \n---------------------------------".format(
            request.user,
            request.get_host(),
            request.path_info,
            request.POST.get("fake-from-domain"),
        )
    )
    res = {"data": None}
    queryset = car.objects.all()
    serializer_class = CarSerializer
    res["data"] = serializer_class(queryset, many=True).data
    return JsonResponse(res)


# class CarViewSet(APIView):
#     # @action(detail=False, methods=["post"])
#     @csrf_exempt
#     def add_car(self, request):
#         res = {"data": None}
#         if carName := request.POST.get("car_name"):
#             car.objects.create(name=carName)
#             res["data"] = {"status": "succeeded"}
#         else:
#             res["data"] = {"error-message": "Please provide a car name."}
#         return JsonResponse(res)
