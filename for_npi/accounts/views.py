from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from .forms import UserSignIn
from django.urls import reverse_lazy

class Login(FormView):
    form_class = UserSignIn
    template_name = 'login.html'
    success_url = reverse_lazy('accounts/your_task.html')
    
    def form_valid(self, form):
        return super().form_valid(form)
    