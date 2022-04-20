from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField(max_length=256)
    username = serializers.CharField(max_length=256)
    identity = serializers.CharField(max_length=16)
    avatar = serializers.ImageField()
