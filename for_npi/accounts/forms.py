from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
User = get_user_model()


class UserSignUp(UserCreationForm):
    role = forms.ChoiceField(choices= Profile.ROLE_CHOICES)
    supervisor = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Supervisor'),
        required=False
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password1', 'password2', 'role', 'supervisor')
        

class UserSignIn(AuthenticationForm):
    pass