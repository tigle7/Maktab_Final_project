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


class ProductListView(ListView):
    model = Product
    template_name = 'shop_dashboard.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.available.filter(owner=self.request.user).order_by('-created_at')
