from django.urls import path
from user_profile import views

app_name= 'user_profile'


urlpatterns = [
    path('tasks_list/', views.Task_List.as_view(), name='tasks_list'),
]