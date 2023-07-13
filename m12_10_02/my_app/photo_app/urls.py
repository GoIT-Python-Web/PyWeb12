from django.urls import path, include

from . import views

app_name = "photo_app"

urlpatterns = [
    path("", views.index, name="main"),  # photo_app:main
    path("images/", views.view_pictures, name="pictures"),
    path("upload/", views.upload, name="upload"),
    path("images/edit/<int:img_id>", views.edit, name="edit"),
    path("images/remove/<int:img_id>", views.remove, name="remove"),
]
