import os
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
def validate_file_size(value):
    filesize = value.size

    if filesize > 1048576:  # 1MB
        raise ValidationError("Максимальний розмір файлу, який можна завантажити - 1MB")
    else:
        return value


def upload_image(instance, filename):
    if instance.user:
        upload_to = instance.user.username
    else:
        upload_to = 'uploads'
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join(upload_to, filename)


class Picture(models.Model):
    description = models.CharField(max_length=200)
    path = models.ImageField(upload_to=upload_image, validators=[validate_file_size])
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
