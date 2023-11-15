from django.urls import path
from accounts import views


urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('signup/', views.UserSignUp.as_view(), name='signup'),
    path('approve-users/', views.approve_users, name='approve_users')
]

