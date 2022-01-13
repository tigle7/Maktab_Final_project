from django.urls import path, re_path
from shop.views.cart_view import CartDetailView, CartListView
from shop.views.product_view import ProductCreateView
from shop.views.shop_view import *
from shop.views.product_view import *

# app_name = 'shop'

urlpatterns = [
    path('', ShopListView.as_view(), name='shop_dashboard'),
    path('create-shop/', ShopCreateView.as_view(), name='create_shop'),
    path('edit-shop/<slug:slug>/', ShopUpdateView.as_view(), name='update_shop'),
    path('delete-shop/<slug:slug>/', ShopDeleteView.as_view(), name='delete_shop'),
    path('<slug:slug>', ShopDetailView.as_view(), name='shop_detail'),
    path('<slug:slug>/add-product', ProductCreateView.as_view(), name='create_product'),
    path('edit-product/<slug:slug>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete-product/<slug:slug>/', ProductDeleteView.as_view(), name='delete_product'),
    path('all-products/', ProductListView.as_view(), name='list_product'),
    path('carts/', CartListView.as_view(), name='list_cart'),
    path('carts/<int:cart_id>', CartDetailView.as_view(), name='list_cart_item'),
]