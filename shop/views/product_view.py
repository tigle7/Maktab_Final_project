from shop.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import (ListView,
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


class ProductListView(LoginRequiredMixin, FilterView):
    model = Product
    template_name = 'pages/product_list.html'
    context_object_name = 'products'
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user, shop__status__in=['C', 'P']).order_by('-created_at')


class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "forms/product_form.html"
    success_message = "Product successfully aded"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.shop = Shop.objects.get(slug=self.kwargs['slug'])
        shop = Shop.objects.get(slug=self.kwargs['slug'])
        if shop.status == 'P':
            messages.warning(
                self.request, "You can't add product to shop with pending status")
            return redirect('shop_dashboard')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ProductCreateView, self).get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs


class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    template_name = "forms/product_form.html"
    fields = ['title', 'category', 'price', 'discount_price',
              'description', 'is_available', 'image']
    success_message = "Product successfully edited"


class ProductDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Product
    template_name = "pages/product_delete.html"

    def get_success_url(self):
        shop_slug = self.object.shop.slug
        messages.success(self.request, f"{self.object.title} successfully deleted")
        return reverse_lazy( 'shop_detail', kwargs = {'slug': shop_slug},)
    
