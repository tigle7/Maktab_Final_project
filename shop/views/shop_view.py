from shop.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import (
    ListView, TemplateView, DetailView, CreateView, DeleteView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from shop.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.decorators import method_decorator

class ShopListView(LoginRequiredMixin, ListView):
    model = Shop
    template_name = 'pages/shop_list.html'
    context_object_name = 'shops'

    def get_queryset(self):
        return Shop.confirmed.filter(owner=self.request.user).order_by('-created_at')

class shopCreateView(LoginRequiredMixin, CreateView):
    pass

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['shop'] = Shop.objects.all()
        context['user'] = User.objects.all()
        return context
