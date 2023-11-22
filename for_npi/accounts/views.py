from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.views import LoginView
from .forms import UserSignIn, UserSignUpForm
from .models import Profile, User
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test


class UserSignUp(FormView):
    form_class = UserSignUpForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()

            role = form.cleaned_data.get('role')
            supervisor = form.cleaned_data.get('supervisor')  # To jest obiekt User

            # Tworzymy profil użytkownika z danymi.
            profile = Profile.objects.create(
                user=user,
                role=role,
                is_approved=False,
            )
            if supervisor:
                profile.supervisor = supervisor
                profile.save()

            # Przypisz użytkownika do odpowiedniej grupy na podstawie roli.
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            return super().form_valid(form)
class Login(LoginView):
    form_class = UserSignIn
    template_name = 'login.html'

    def form_valid(self, form):
        # Sprawdzanie, czy użytkownik ma zatwierdzony profil
        user = form.get_user()
        try:
            profile = user.profile
            if not profile.is_approved:
                form.add_error(None, "Twoje konto oczekuje na zatwierdzenie przez nadzorcę.")
                return super().form_invalid(form)
            
        except Profile.DoesNotExist:
            form.add_error(None, "Profil użytkownika nie istnieje.")
            return super().form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('user_profile:main_page')
    

def is_supervisor(user):
    return user.groups.filter(name='Supervisor').exists()  
    
@login_required    
def supervisorview(request):
    is_supervisor = request.user.groups.filter(name='Supervisor').exists() 
    return render(request, 'approve_users.html', {'is_supervisor': is_supervisor})

    
@login_required
@user_passes_test(is_supervisor)
def approve_users(request):
    profiles_to_approve = Profile.objects.filter(supervisor=request.user, is_approved=False)
    if request.method=='POST':
        profile_id = request.POST.get('profile_id')
        profile_to_approve = get_object_or_404(Profile, id=profile_id)
        profile_to_approve.is_approved = True
        profile_to_approve.save()
        return redirect('approve_users')  

    return render(request, 'approve_users.html', {'profiles': profiles_to_approve})
        
    
def subordinates_view(request):
    subordinates = Profile.objects.filter(supervisor=request.user, is_approved=True)
    return render(request, 'subordinates.html', {'subordinates': subordinates})