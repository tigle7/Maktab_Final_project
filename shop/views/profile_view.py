from pipes import Template
from re import template
from shop.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import (ListView, TemplateView,
                                  DetailView, CreateView, DeleteView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from shop.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django_filters.views import FilterView
from shop.filters import ProductFilter
from user.models import CustomUser

class ProfileView(LoginRequiredMixin, TemplateView):
    model = CustomUser
    template_name = 'pages/profile.html'

class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "forms/profile_form.html"
    success_url = reverse_lazy("profile")
    form_class = ProfileForm
    model = CustomUser

    def get_object(self, queryset=None):
        return self.request.user