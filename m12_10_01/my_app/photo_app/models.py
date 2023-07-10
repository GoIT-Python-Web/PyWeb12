from django.db import models

# Create your models here.


class Picture(models.Model):
    description = models.CharField(max_length=200)
    path = models.ImageField(upload_to='images')
