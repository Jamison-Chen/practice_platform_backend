from rest_framework import serializers


class CarSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
