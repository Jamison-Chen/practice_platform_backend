import uuid
import os

from django.db import models


class CreateUpdateDate(models.Model):
    """
    Abstract base class with a creation and modification date and time
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def upload_to(instance, filename):
    base, extension = os.path.splitext(filename)
    return "brand_logos/{}".format(instance.id + extension)


class tenant(CreateUpdateDate):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    domain_name = models.CharField(max_length=256, unique=True)
    schema_name = models.CharField(max_length=1024, unique=True)
    brand_name = models.CharField(max_length=64, blank=True, null=True)
    tax_id_number = models.CharField(max_length=16, blank=True, null=True)
    logo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    tel = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return self.domain_name
