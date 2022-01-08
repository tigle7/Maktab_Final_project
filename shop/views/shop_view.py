from django.contrib.messages.api import success
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
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy

class ShopListView(LoginRequiredMixin, ListView):
    model = Shop
    template_name = 'pages/shop_list.html'
    context_object_name = 'shops'

    def get_queryset(self):
        return Shop.confirmed.filter(owner=self.request.user).order_by('-created_at')


class ShopCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Shop
    form_class = ShopForm
    template_name = 'forms/shop_form.html'
    success_message = "Your Shop successfully created wait for confirm"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        pending_shop_count = Shop.objects.filter(status='P', owner=self.request.user).count()
        if not self.request.user.is_seller:
            messages.warning(
                    self.request, f"Dear {self.request.user.username} your account not verified yet")
            return redirect('shop_dashboard')
        if pending_shop_count:
            messages.warning(
                    self.request, f"You already have {pending_shop_count} Shop with pending status")
            return redirect('shop_dashboard')
        # print(pending_shop_count)
        # form.instance.image = self.request.FILES['image']
        return super().form_valid(form)

    # def get_form_kwargs(self):
    #     kwargs = super(ShopCreateView, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs


class ShopUpdateView(LoginRequiredMixin, UpdateView):
    model = Shop
    fields = ['title', 'type', 'image',]
    template_name = "forms/shop_form.html"
    success_url = "/dashboard/"

    def form_valid(self, form):
        form.instance.status = "P"
        return super().form_valid(form)


class ShopDeleteView(LoginRequiredMixin, DeleteView):
    model = Shop
    template_name = "pages/shop_delete.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = 'D'
        self.object.save()
        return redirect(reverse('shop_dashboard'))

class ShopDetailView(LoginRequiredMixin, DetailView):
    model = Shop
    template_name = 'pages/shop_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop']= Shop.objects.get(slug=self.kwargs['slug'], status__in=['C', 'P'])
        context['products'] = Product.objects.filter(shop__slug=self.kwargs['slug'])
        return context


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['shop'] = Shop.objects.all()
        context['user'] = User.objects.all()
        return context
