from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import TodoForm
from .models import Todo


# Create your views here.
class TodoListView(ListView):
    model = Todo
    template_name = "todo/list.html"
    context_object_name = "todo_list"
    paginate_by = 5


class TodoCreateView(CreateView):
    model = Todo
    template_name = "todo/create.html"
    form_class = TodoForm
    success_url = reverse_lazy('main')

    # def get_queryset(self):
    #     queryset = super(TodoCreateView, self).get_queryset()
    #     return queryset


class TodoUpdateView(UpdateView):
    model = Todo
    template_name = "todo/update.html"
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('main')


class TodoDeleteView(DeleteView):
    model = Todo
    template_name = "todo/delete.html"
    success_url = reverse_lazy('main')
