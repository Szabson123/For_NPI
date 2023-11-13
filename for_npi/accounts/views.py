from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.contrib.auth.views import LoginView
from .forms import UserSignIn, UserSignUp
from .models import Profile
from django.urls import reverse_lazy
from django.db import transaction


class UserSignUp(FormView):
    form_class = UserSignUp
    template_name = 'sign_up.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()
            Profile.objects.create(user=user, role=form.cleaned_data['role'], is_approved=False)
            return super().form_valid(form)
    

class Login(LoginView):
    form_class = UserSignIn
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('user_profile:main_page')
    
    