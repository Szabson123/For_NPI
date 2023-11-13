from django.urls import path
from user_profile import views
from django.contrib.auth.views import LogoutView

app_name = 'user_profile'


urlpatterns = [
    path('main_page/', views.MainPage.as_view(), name='main_page'),
    path('tasks_list/', views.TaskList.as_view(), name='tasks_list'),
    path('task_form/', views.TaskForm.as_view(), name='task_form'),

    path('logout/', LogoutView.as_view(), name='logout')
]