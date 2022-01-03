from django.urls import path, re_path
from .views import *
from django.contrib.auth import views
# app_name = 'user'

urlpatterns = [
    path('register/', register, name='register'),
    path('', Login.as_view(template_name='login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]