from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import TaskForm, ProductionIssueForm
from django.urls import reverse_lazy
from .models import Task, ProductionIssue
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.functions import TruncDate
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from accounts.models import Profile


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
    


@login_required
def accept_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.accepted_date = timezone.now()
        task.save()
        return redirect('user_profile:task_detail', pk=pk)  
    else:
        return redirect('user_profile:tasks_list')  


@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.completed_date = timezone.now()
        task.save()
        return redirect('user_profile:history_view')
    else:
        return redirect('user_profile:tasks_list')



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
    completed_tasks = Task.objects.filter(completed_date__isnull=False).annotate(completed_date_date=TruncDate('completed_date')).order_by('-completed_date_date')

    grouped_tasks = {}
    for task in completed_tasks:
        completed_date = task.completed_date_date
        if completed_date not in grouped_tasks:
            grouped_tasks[completed_date] = []
        grouped_tasks[completed_date].append(task)

    return render(request, 'user_profile/history_view.html', {'grouped_tasks': grouped_tasks})


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
        return self.request.user.groups.filter(name='Supervisor').exists()

    def post(self, request, issue_id):
        subordinate_id = request.POST.get('subordinate')
        issue = get_object_or_404(ProductionIssue, pk=issue_id)
        issue.assigned_to_id = subordinate_id
        issue.save()
        return redirect('user_profile:main_page')


