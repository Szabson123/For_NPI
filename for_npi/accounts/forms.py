from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
User = get_user_model()


class UserSignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)
    supervisor = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Supervisor'),
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'role', 'supervisor')

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        self.fields['supervisor'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"
        

class UserSignIn(AuthenticationForm):
    pass