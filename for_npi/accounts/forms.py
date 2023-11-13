from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

User = get_user_model()

class UserSignIn(UserCreationForm):
    role = forms.ChoiceField(choices= Profile.ROLE_CHOICES)
    
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'role')
        