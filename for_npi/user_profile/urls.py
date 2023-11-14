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
    
     path('profile/<str:username>/', views.UserProfileView.as_view(), name='profile'),
    
]
