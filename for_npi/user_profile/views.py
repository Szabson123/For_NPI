from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import TaskForm, ProductionIssueForm, IssueFilterForm, IssueFixForm, DateFilterForm, UserProfileForm
from django.urls import reverse_lazy, reverse
from .models import Task, ProductionIssue, IssueFix, TaskCompletion
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.functions import TruncDate
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from accounts.models import Profile
from django.contrib import messages


def history_issue_list(request):
    form = IssueFilterForm(request.GET or None)
    issues = ProductionIssue.objects.all()

    if form.is_valid():
        title = form.cleaned_data.get('title')
        status = form.cleaned_data.get('status')
        priority = form.cleaned_data.get('priority')
        line = form.cleaned_data.get('line')
        machine = form.cleaned_data.get('machine')
        type_of_issue = form.cleaned_data.get('type_of_issue')
        reported_by = form.cleaned_data.get('reported_by')
        accepted_by = form.cleaned_data.get('accepted_by')

        if title:
            issues = issues.filter(title__icontains=title)
        if status:
            issues = issues.filter(status=status)
        if priority:
            issues = issues.filter(priority=priority)
        if line:
            issues = issues.filter(line=line)
        if machine:
            issues = issues.filter(machine=machine)
        if type_of_issue:
            issues = issues.filter(type_of_issue=type_of_issue)
        if reported_by:
            issues = issues.filter(reported_by=reported_by)
        if accepted_by:
            issues = issues.filter(accepted_by=accepted_by)

    return render(request, 'user_profile/history_issue_list.html', {'form': form, 'issues': issues})


class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'user_profile/tasks_list.html'
    
    def get_queryset(self):
        return Task.objects.filter(
            Q(author=self.request.user) | Q(assigned_to=self.request.user)).distinct()


class TaskCreateView(CreateView, LoginRequiredMixin):
    form_class = TaskForm
    template_name = 'user_profile/task_form.html'
    success_url = reverse_lazy('user_profile:tasks_list')

    def get_form_kwargs(self):
        kwargs = super(TaskCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request  # Dodajemy request do argumentów formularza
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user  # Ustawienie autora zadania na aktualnie zalogowanego użytkownika
        return super().form_valid(form)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'user_profile/task_form.html'
    success_url = reverse_lazy('user_profile:tasks_list')


class TaskDetailView(DetailView):
    model = Task
    template_name = 'user_profile/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['is_supervisor'] = self.request.user == task.author # Sprawdza, czy użytkownik to przełożony
        context['assigned_users'] = task.assigned_to.all() # Lista użytkowników przypisanych do zadania
        context['is_user_assigned'] = task.assigned_to.filter(id=self.request.user.id).exists()
        return context
    


@login_required(login_url='login')
def accept_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.accepted_by.add(request.user)
        task.accepted_date = timezone.now()
        task.save()
        return redirect('user_profile:task_detail', pk=pk)
    else:
        return redirect('user_profile:tasks_list')


@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.completed_by.add(request.user)
        task.completed_date = timezone.now()
        task.save()
        return redirect('user_profile:task_detail', pk=pk)
    else:
        return redirect('user_profile:tasks_list')

@login_required
def finalize_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user.is_supervisor and task.ready_for_supervisor_review:
        if request.method == 'POST':
            task.is_completed = True
            task.completed_date = timezone.now()
            task.save()
            return redirect('user_profile:tasks_list')
    return redirect('user_profile:task_detail', pk=task.pk)

@login_required
def tasks_list(request):
    if request.user.is_supervisor:
        tasks = Task.objects.filter(is_completed=False, ready_for_supervisor_review=False)
    else:
        tasks = Task.objects.filter(is_completed=False, assigned_to=request.user)

    return render(request, 'user_profile/tasks_list.html', {'tasks': tasks})
class MainPage(TemplateView):
    template_name = 'user_profile/main_page.html'



class UserProfileView(DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'user_profile/user_profile.html'
    
    

@login_required
def create_task_for_subordinate(request, username):
    subordinate = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            task.assigned_to.set([subordinate])
            return redirect('user_profile:tasks_list')
    else:
        form = TaskForm(initial={'assigned_to': [subordinate]})
    return render(request, 'user_profile/task_form.html', {'form': form})



@login_required
def history_view(request):
    completed_tasks = Task.objects.filter(author=request.user, completed_date__isnull=False).order_by('-completed_date')
    return render(request, 'user_profile/history_view.html', {'completed_tasks': completed_tasks})


class ProductionIssueCreateView(CreateView):
    model = ProductionIssue
    form_class = ProductionIssueForm
    template_name = 'user_profile/production_issue_form.html'
    success_url = reverse_lazy('user_profile:main_page')

    def form_valid(self, form):
        form.instance.reported_by = self.request.user
        return super().form_valid(form)


class ProductionIssueListView(LoginRequiredMixin, ListView):
    model = ProductionIssue
    template_name = 'user_profile/main_page.html'

    def get_queryset(self):
        return ProductionIssue.objects.all().order_by('-report_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subordinates'] = Profile.objects.filter(supervisor=self.request.user, is_approved=True)
        return context


class IssueAcceptView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Supervisor').exists()

    def post(self, request, pk):
        issue = get_object_or_404(ProductionIssue, pk=pk)
        issue.status = 'closed'
        issue.save()
        return redirect('user_profile:main_page')


class IssueAssignView(UserPassesTestMixin, View):
    def test_func(self):
        # Twoje istniejące warunki testowe...
        return self.request.user.groups.filter(name='Supervisor').exists()

    def post(self, request, pk):
        issue = get_object_or_404(ProductionIssue, pk=pk)
        user_id = request.POST.get('subordinate')
        user = get_object_or_404(User, pk=user_id)
        issue.assigned_to = user
        issue.accepted_by = user  # Przydzielającemu automatycznie staje się akceptantem
        issue.accepted_date = timezone.now()  # Ustaw aktualną datę jako datę akceptacji
        issue.save()
        return redirect('user_profile:main_page')


@login_required
def accept_issue(request, pk):
    issue = get_object_or_404(ProductionIssue, pk=pk)
    if request.method == 'POST':
        if not issue.accepted_date:  # Sprawdź, czy problem nie został już zaakceptowany
            issue.accepted_date = timezone.now()
            issue.accepted_by = request.user  # Zapisz użytkownika, który zaakceptował problem
            issue.save()
        return redirect('user_profile:main_page')
    else:
        return redirect('user_profile:main_page')


@login_required
def complete_issue(request, pk):
    issue = get_object_or_404(ProductionIssue, pk=pk)
    if request.method == 'POST':
        if not issue.completed_date:  # Jeśli zadanie nie zostało jeszcze zakończone
            issue.completed_date = timezone.now()
            issue.status = 'closed'  # Ustaw status na 'closed'
            issue.save()
            messages.success(request, 'Zadanie zostało zakończone i zamknięte.')  # Wiadomość o sukcesie
        else:
            messages.warning(request, 'Zadanie zostało już zakończone.')  # Wiadomość, jeśli zadanie było już zakończone
        return redirect('user_profile:history_issue_list')  # Przekieruj do strony z historią zadań
    else:
        messages.error(request, 'Nieprawidłowe żądanie.')  # Wiadomość o błędzie, jeśli żądanie nie jest POST
        return redirect('user_profile:history_issue_list')  # Przekieruj z powrotem do strony z historią zadań


def issue_fix_create_view(request, issue_id):
    issue = get_object_or_404(ProductionIssue, id=issue_id)

    # Sprawdź, czy zgłoszenie nie zostało już zamknięte
    if issue.status == 'closed':
        messages.error(request, 'To zgłoszenie zostało już zamknięte.')
        return redirect('user_profile:history_issue_list')

    if request.method == 'POST':
        form = IssueFixForm(request.POST)
        if form.is_valid():
            issue_fix = form.save(commit=False)
            issue_fix.production_issue = issue

            # Tutaj zamykamy zgłoszenie
            issue.completed_date = timezone.now()
            issue.status = 'closed'
            issue.save()

            issue_fix.save()
            messages.success(request, 'Rozwiązanie problemu zostało zapisane i zgłoszenie zostało zamknięte.')
            return redirect('user_profile:history_issue_list')
    else:
        form = IssueFixForm()

    return render(request, 'user_profile/issue_fix_form.html', {'form': form, 'issue': issue})




def issue_detail_view(request, issue_id):
    issue = get_object_or_404(ProductionIssue, id=issue_id)
    issue_fix = IssueFix.objects.filter(production_issue=issue).first()

    return render(request, 'user_profile/issue_detail.html', {
        'issue': issue,
        'issue_fix': issue_fix,
    })
    
    
def issue_list_filtered_by_date(request):
    issues = ProductionIssue.objects.all()
    form = DateFilterForm(request.GET or None)
    
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        
        if start_date:
            issues = issues.filter(report_date__date__gte=start_date)
        if end_date:
            issues = issues.filter(report_date__date__lte=end_date)
    else:
        form.fields['end_date'].initial = timezone.localdate()
    
    context = {
        'form': form,
        'issues': issues
    }
    return render(request, 'user_profile/history_issue_list.html', context)


@login_required
def edit_user_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            username = request.user.username
            return redirect(reverse('user_profile:profile', kwargs={'username': username}))
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'user_profile/edit_profile.html', {'form': form})
