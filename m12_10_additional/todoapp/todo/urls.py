from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.TodoListView.as_view(), name="main"),
    path("list/<int:page>", views.TodoListView.as_view(), name="todolist"),
    path("todo/create", views.TodoCreateView.as_view(), name="create-todo"),
    path("todo/update/<pk>", views.TodoUpdateView.as_view(), name="update-todo"),
    path("todo/delete/<pk>", views.TodoDeleteView.as_view(), name="delete-todo"),
]