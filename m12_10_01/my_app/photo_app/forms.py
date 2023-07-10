from django.forms import ModelForm, ImageField, CharField, TextInput, FileInput

from .models import Picture


class PictureForm(ModelForm):
    description = CharField(max_length=200, min_length=5, widget=TextInput(attrs={"class": "form-control"}))
    path = ImageField(widget=FileInput(attrs={"class": "form-control", "accept": "image/*"}))

    class Meta:
        model = Picture
        fields = ['description', 'path']
