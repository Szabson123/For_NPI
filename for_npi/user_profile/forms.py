from .models import Task
from django import forms
from accounts.models import User
from .models import ProductionIssue, IssueFix
from django.db.models import Exists, OuterRef
import datetime
from accounts.models import Profile

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'text', 'priority', 'additional', 'assigned_to', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.TextInput(attrs={'class': 'form-control', 'rows': 3}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'additional': forms.TextInput(attrs={'class': 'form-control'}),
            'assigned_to': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        # Sprawdzamy, czy zalogowany użytkownik jest w grupie "Supervisor"
        if request and request.user.groups.filter(name='Supervisor').exists():
            self.fields['assigned_to'].queryset = User.objects.filter(profile__supervisor=request.user)
        else:
            del self.fields['assigned_to']


class ProductionIssueForm(forms.ModelForm):
    class Meta:
        model = ProductionIssue
        fields = ['title', 'description', 'priority', 'line', 'machine', 'type_of_issue']  # Dodaj nowe pola
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'line': forms.TextInput(attrs={'class': 'form-control'}),  # Dodaj odpowiednie atrybuty dla nowych pól
            'machine': forms.TextInput(attrs={'class': 'form-control'}),
            'type_of_issue': forms.TextInput(attrs={'class': 'form-control'})
        }



class IssueFilterForm(forms.Form):
    # Stałe choices dla statusu i priorytetu
    STATUS_CHOICES = [('', 'Any Status'), ('open', 'Open'), ('closed', 'Closed')]
    PRIORITY_CHOICES = [('', 'Any Priority'), ('high', 'High'), ('medium', 'Medium'), ('low', 'Low')]

    title = forms.CharField(required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    line = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    machine = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    type_of_issue = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    reported_by = forms.ModelChoiceField(queryset=User.objects.none(), required=False, label='Reported by', widget=forms.Select(attrs={'class': 'form-control'}))
    accepted_by = forms.ModelChoiceField(queryset=User.objects.none(), required=False, label='Accepted by', widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(IssueFilterForm, self).__init__(*args, **kwargs)
        # Dynamiczne ustawienie choices dla line, machine i type_of_issue
        self.fields['line'].choices = [('', 'Any Line')] + [(line, line) for line in ProductionIssue.objects.values_list('line', flat=True).distinct()]
        self.fields['machine'].choices = [('', 'Any Machine')] + [(machine, machine) for machine in ProductionIssue.objects.values_list('machine', flat=True).distinct()]
        self.fields['type_of_issue'].choices = [('', 'Any Type of Issue')] + [(issue_type, issue_type) for issue_type in ProductionIssue.objects.values_list('type_of_issue', flat=True).distinct()]

        # Dynamiczne ustawienie queryset dla reported_by i accepted_by
        self.fields['reported_by'].queryset = User.objects.filter(Exists(ProductionIssue.objects.filter(reported_by=OuterRef('pk')))).distinct()
        self.fields['accepted_by'].queryset = User.objects.filter(Exists(ProductionIssue.objects.filter(accepted_by=OuterRef('pk')))).distinct()

        # Ustawienie funkcji formatującej wyświetlanie użytkowników
        self.fields['reported_by'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"
        self.fields['accepted_by'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"


    def label_from_user_instance(self, obj):
        profile = obj.profile
        return f"{profile.user.first_name} {profile.user.last_name}"


class IssueFixForm(forms.ModelForm):
    class Meta:
        model = IssueFix
        fields = ['cause', 'action']
        widgets = {
            'cause': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'action': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'cause': "Przyczyna",
            'action': "Co zrobiłeś, żeby naprawić",
        }
        
        
class DateInput(forms.DateInput):
    input_type = 'date'
    

class DateFilterForm(forms.Form):
    start_date = forms.DateField(widget=DateInput(), required=False)
    end_date = forms.DateField(widget=forms.DateInput(), required=False, initial=datetime.date.today)
    

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['position', 'supervisor', 'department', 'phone_number', 'office_number', 'languages']
        widgets = {
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            # Dodaj klasy 'form-control' dla pozostałych pól
        }
        
        