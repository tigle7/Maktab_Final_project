from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f"Dear {username} your account successfully has been created let's login :)")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


class Login(LoginView):

    def get_success_url(self):
        user = self.request.user
        return reverse('dashboard', args = [str(self.request.user.username)])
