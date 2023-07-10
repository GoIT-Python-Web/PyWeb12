from django.shortcuts import render, redirect

from .forms import PictureForm
from .models import Picture


# Create your views here.
def index(request):
    return render(request, "photo_app/index.html", context={"title": "Main Page"})


def view_pictures(request):
    pictures = Picture.objects.all()
    return render(request, "photo_app/pictures.html", context={"title": "Pictures Page",
                                                               "pictures": pictures})


def upload(request):
    form = PictureForm(instance=Picture())
    if request.method == "POST":
        form = PictureForm(request.POST, request.FILES, instance=Picture())
        if form.is_valid():
            form.save()
            return redirect(to="photo_app:pictures")
    return render(request, "photo_app/upload.html", context={"title": "Upload Page", "form": form})
