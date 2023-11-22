from .models import Task
from django import forms
from accounts.models import User
from .models import ProductionIssue


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
    STATUS_CHOICES = [
        ('', 'Any Status'),  # Default choice
        ('open', 'Open'),
        ('closed', 'Closed'),
        # Dodaj więcej statusów jeśli potrzebujesz
    ]

    PRIORITY_CHOICES = [
        ('', 'Any Priority'),  # Default choice
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        # Dodaj więcej priorytetów jeśli potrzebujesz
    ]

    title = forms.CharField(required=False)
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False)