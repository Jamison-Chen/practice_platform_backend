# import os

from django.db import models


# def upload_to(instance, filename):
#     base, extension = os.path.splitext(filename)
#     return "test_car/{}".format(instance.id + extension)


class car(models.Model):
    name = models.CharField(max_length=128)
    # image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    # image_url = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.name
