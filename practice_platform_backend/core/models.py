import uuid
import os
import datetime

from django.db import models


class CreateUpdateDateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SortableModel(models.Model):
    order_number = models.PositiveIntegerField()

    class Meta:
        abstract = True


class PublishableModel(models.Model):
    publication_date = models.DateField(blank=True, null=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @property
    def is_visible(self):
        return self.is_published and (
            self.publication_date is None
            or self.publication_date <= datetime.date.today()
        )


def upload_to(instance, filename):
    base, extension = os.path.splitext(filename)
    return "brand_logos/{}".format(str(instance.id) + filename)


class tenant(CreateUpdateDateModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    domain_name = models.CharField(max_length=256, unique=True)
    schema_name = models.CharField(max_length=1024, unique=True)
    brand_name = models.CharField(max_length=64, blank=True, null=True)
    tax_id_number = models.CharField(max_length=16, blank=True, null=True)
    logo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    tel = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return self.domain_name
