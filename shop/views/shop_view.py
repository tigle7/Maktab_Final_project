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
from django.db.models import Count, Sum


class ShopListView(LoginRequiredMixin, ListView):
    model = Shop
    template_name = 'pages/shop_list.html'
    context_object_name = 'shops'

    def get_queryset(self):
        return Shop.confirmed.filter(owner=self.request.user).annotate(product_count=Count('product_shop')).order_by('-created_at')


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
            return redirect('shop_list')
        if pending_shop_count:
            messages.warning(
                    self.request, f"You already have {pending_shop_count} Shop with pending status")
            return redirect('shop_list')
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
    success_url = "/dashboard/shops/"

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
        return redirect(reverse('shop_list'))

class ShopDetailView(LoginRequiredMixin, DetailView):
    model = Shop
    template_name = 'pages/shop_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop']= Shop.objects.get(slug=self.kwargs['slug'], status__in=['C', 'P'])
        context['products'] = Product.objects.filter(shop__slug=self.kwargs['slug'])
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/dashboard.html'

    def get_context_data(self, *args, **kwargs):

        carts = Cart.objects.filter(items__product__owner=self.request.user, status='P').distinct()
        # print(carts)
        shop_total_sell = {}
        shop_totall_sell = 0
        for cart in carts:
            for shop, total_price in cart.each_shop_total_price.items():
                if shop.owner == self.request.user:
                    # shop_totall_sell += total_price
                    if shop in shop_total_sell:
                        shop_total_sell[shop.title] += total_price
                    else:
                        shop_total_sell[shop.title] = total_price
            # shop_total_sell[cart] = shop_totall_sell
            # print(shop_totall_sell)
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['shops'] = Shop.confirmed.filter(owner=self.request.user).annotate(total_sell=Sum('cart__items__price')).order_by('-created_at')
        context['shop_total_sell'] = shop_total_sell
        return context
