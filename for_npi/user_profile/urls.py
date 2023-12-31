from django.urls import path
from user_profile import views
from django.contrib.auth.views import LogoutView

app_name = 'user_profile'


urlpatterns = [
    path('main_page/', views.MainPage.as_view(), name='main_page'),
    path('tasks_list/', views.TaskListView.as_view(), name='tasks_list'),
    path('task_form/', views.TaskCreateView.as_view(), name='task_form'),

    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('task_detail/<int:pk>', views.TaskDetailView.as_view(), name='task_detail'),
    path('task_update/<int:pk>', views.TaskUpdateView.as_view(), name='task_update'),
    path('task_accept/<int:pk>/', views.accept_task, name='task_accept'),
    path('task_complete/<int:pk>/', views.complete_task, name='task_complete'),
    path('history_view/', views.history_view, name='history_view'),
    path('task/finalize/<int:pk>/', views.finalize_task, name='finalize_task'),

    path('profile/<str:username>/', views.UserProfileView.as_view(), name='profile'),
    path('task/create-for/<str:username>/', views.create_task_for_subordinate, name='create_task_for_subordinate'),

    path('issues/create/', views.ProductionIssueCreateView.as_view(), name='issue_create'),
    path('issues/', views.ProductionIssueListView.as_view(), name='main_page'),
    path('issue_accept/<int:pk>/', views.accept_issue, name='issue_accept'),
    path('issue_complete/<int:pk>/', views.complete_issue, name='issue_complete'),
    path('issue_assign/<int:pk>/', views.IssueAssignView.as_view(), name='issue_assign'),
    path('history_issue_list/', views.history_issue_list, name='history_issue_list'),

    path('issue/<int:issue_id>/fix/', views.issue_fix_create_view, name='issue_fix_create'),
    path('issue/<int:issue_id>/', views.issue_detail_view, name='issue_detail'),
    
    path('edit-profile/', views.edit_user_profile, name='edit_profile'),
]
