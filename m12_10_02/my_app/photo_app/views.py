import os

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import PictureForm
from .models import Picture


# Create your views here.
def index(request):
    return render(request, "photo_app/index.html", context={"title": "Main Page"})


@login_required
def view_pictures(request):
    pictures = Picture.objects.filter(user=request.user).all()
    return render(request, "photo_app/pictures.html", context={"title": "Pictures Page",
                                                               "pictures": pictures})


@login_required
def upload(request):
    form = PictureForm(instance=Picture())
    if request.method == "POST":
        form = PictureForm(request.POST, request.FILES, instance=Picture())
        if form.is_valid():
            picture = form.save(commit=False)
            picture.user = request.user
            picture.save()
            return redirect(to="photo_app:pictures")
    return render(request, "photo_app/upload.html", context={"title": "Upload Page", "form": form})


@login_required
def edit(request, img_id):
    if request.method == "POST":
        description = request.POST.get("description")
        Picture.objects.filter(pk=img_id, user=request.user).update(description=description)
        return redirect(to="photo_app:pictures")

    pic = Picture.objects.filter(pk=img_id, user=request.user).first()
    return render(request, "photo_app/change.html", context={"title": "Change description", "pic": pic})


@login_required
def remove(request, img_id):
    pic = Picture.objects.filter(pk=img_id, user=request.user)
    try:
        os.unlink(os.path.join(settings.MEDIA_ROOT, str(pic.first().path)))
    except OSError as e:
        print(e)
    pic.delete()
    return redirect(to="photo_app:pictures")
