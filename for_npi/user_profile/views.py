from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class TaskList(TemplateView):
    template_name = 'user_profile/tasks_list.html'


class TaskForm(TemplateView):
    template_name = 'user_profile/task_form.html'


class MainPage(TemplateView):
    template_name = 'user_profile/main_page.html'
