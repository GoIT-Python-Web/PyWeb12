from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
def validate_file_size(value):
    filesize = value.size

    if filesize > 1048576:  # 1MB
        raise ValidationError("Максимальний розмір файлу, який можна завантажити - 1MB")
    else:
        return value


class Picture(models.Model):
    description = models.CharField(max_length=200)
    path = models.ImageField(upload_to='images', validators=[validate_file_size])
