import uuid
import os

from django.db import models

from ..seo.models import SeoModel
from ..core.models import CreateUpdateDateModel, PublishableModel, SortableModel


class article(PublishableModel, CreateUpdateDateModel, SeoModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self) -> str:
        return self.title


def upload_to(instance, filename):
    base, extension = os.path.splitext(filename)
    return "article_images/{}/{}".format(
        instance.article.title, str(instance.id) + filename
    )


class paragraph(SortableModel):
    article = models.ForeignKey(
        article, related_name="paragraphs", on_delete=models.CASCADE
    )
    text = models.TextField(blank=True, null=True)
    image = models.ImageField()

    def __str__(self) -> str:
        return "Paragraph of {}".format(self.article.title)
