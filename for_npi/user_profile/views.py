from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class Task_List(TemplateView):
    template_name = 'user_profile/tasks_list.html'