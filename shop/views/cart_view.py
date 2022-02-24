from unicodedata import category
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
from shop.filters import *

class CartListView(LoginRequiredMixin, FilterView):
    model = Cart
    template_name = 'pages/cart_list.html'
    context_object_name = 'carts'
    filterset_class = CartFilter

    def get_queryset(self):
        carts = Cart.objects.filter(items__product__owner=self.request.user).distinct()
        print(carts)
        each_seller_cart = {}
        for cart in carts:
            seller_total_price = 0
            for shop, total_price in cart.each_shop_total_price.items():
                if shop.owner == self.request.user:
                    seller_total_price += total_price
            each_seller_cart[cart] = seller_total_price
            # print(seller_total_price)
        print (each_seller_cart)


            # print (cart.each_shop_total_price)
        return carts
    

class CartDetailView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = "pages/cartItems_list.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart']= Cart.objects.get(id=self.kwargs['cart_id'])
        context['cart_items'] = CartItem.objects.filter(cart__id=self.kwargs['cart_id'], product__owner=self.request.user)

        # items = CartItem.objects.filter(cart__id=self.kwargs['cart_id'], product__owner=self.request.user)
        # total = 0
        # for item in items:
        #     total += item.total_price


        return context