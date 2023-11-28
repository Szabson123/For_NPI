from .models import Task
from django import forms
from accounts.models import User
from .models import ProductionIssue, IssueFix
from django.db.models import Exists, OuterRef

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
    line_choices = [('', 'Any Line')] + [(line, line) for line in ProductionIssue.objects.values_list('line', flat=True).distinct()]
    machine_choices = [('', 'Any Machine')] + [(machine, machine) for machine in ProductionIssue.objects.values_list('machine', flat=True).distinct()]
    type_of_issue_choices = [('', 'Any Type of Issue')] + [(issue_type, issue_type) for issue_type in ProductionIssue.objects.values_list('type_of_issue', flat=True).distinct()]

    line = forms.ChoiceField(choices=line_choices, required=False)
    machine = forms.ChoiceField(choices=machine_choices, required=False)
    type_of_issue = forms.ChoiceField(choices=type_of_issue_choices, required=False)

    reported_by = forms.ModelChoiceField(
        queryset=User.objects.filter(
            Exists(ProductionIssue.objects.filter(reported_by=OuterRef('pk')))
        ).distinct(),
        required=False,
        label='Reported by'
    )

    accepted_by = forms.ModelChoiceField(
        queryset=User.objects.filter(
            Exists(ProductionIssue.objects.filter(accepted_by=OuterRef('pk')))
        ).distinct(),
        required=False,
        label='Accepted by'
    )

    def __init__(self, *args, **kwargs):
        super(IssueFilterForm, self).__init__(*args, **kwargs)
        self.fields['reported_by'].label_from_instance = self.label_from_user_instance
        self.fields['accepted_by'].label_from_instance = self.label_from_user_instance

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