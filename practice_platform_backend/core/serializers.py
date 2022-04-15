from rest_framework import serializers


class TenantSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    domain_name = serializers.CharField(max_length=256)
    schema_name = serializers.CharField(max_length=1024)
    brand_name = serializers.CharField(max_length=64)
    tax_id_number = serializers.CharField(max_length=16)
    logo = serializers.ImageField()
    tel = serializers.CharField(max_length=16)
