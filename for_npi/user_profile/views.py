from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import TaskForm
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin


class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'user_profile/tasks_list.html'


class TaskCreateView(CreateView, LoginRequiredMixin):
    form_class = TaskForm
    template_name = 'user_profile/task_form.html'
    success_url = reverse_lazy('user_profile:tasks_list')

    def form_valid(self, form):
        form.instance.author = self.request.user  # Ustawienie autora zadania na aktualnie zalogowanego użytkownika
        return super().form_valid(form)


class TaskUpdateView(UpdateView):
    form_class = TaskForm
    template_name = 'user_profile/task_form.html'
    success_url = reverse_lazy('task_list')


class TaskDetailView(DetailView):
    model = Task
    template_name = 'user_profile/task_detail.html'
    context_object_name = 'task'



class MainPage(TemplateView):
    template_name = 'user_profile/main_page.html'
