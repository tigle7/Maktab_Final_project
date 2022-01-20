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
from django.db.models import Count


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'pages/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(author=user).annotate(product_count=Count('product_category'))


class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'forms/category_form.html'
    success_message = "Category successfully aded"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Category
    fields = ['title', 'parent']
    template_name = 'forms/category_form.html'
    success_message = "Category successfully edited"


class CategoryDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Category
    template_name = 'pages/category_delete.html'
    success_url = reverse_lazy('list_category')
    success_message = "successfully deleted"

    def test_func(self):
        category = self.get_object()
        if self.request.user == category.author:
            return True
        return False
