import uuid

from django.db import models


class tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    domain_name = models.CharField(max_length=256, unique=True)
    schema_name = models.CharField(max_length=1024, unique=True)

    def __str__(self):
        return self.domain_name
