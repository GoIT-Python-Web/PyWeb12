from django.db import models


# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=250)
    completed = models.BooleanField(default=False)
    published = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.title
