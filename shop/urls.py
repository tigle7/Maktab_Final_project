from django.urls import path, re_path
from shop.views.cart_view import CartDetailView, CartListView
from shop.views.product_view import ProductCreateView
from shop.views.shop_view import *
from shop.views.product_view import *
from shop.views.category_view import *
from shop.views.profile_view import *

# app_name = 'shop'

urlpatterns = [
    path('', ShopListView.as_view(), name='shop_dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit-profile/', ProfileUpdateView.as_view(), name='update_profile'),
    path('<slug:slug>', ShopDetailView.as_view(), name='shop_detail'),
    path('<slug:slug>/add-product', ProductCreateView.as_view(), name='create_product'),
    path('create-shop/', ShopCreateView.as_view(), name='create_shop'),
    path('edit-shop/<slug:slug>/', ShopUpdateView.as_view(), name='update_shop'),
    path('delete-shop/<slug:slug>/', ShopDeleteView.as_view(), name='delete_shop'),
    path('edit-product/<slug:slug>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete-product/<slug:slug>/', ProductDeleteView.as_view(), name='delete_product'),
    path('all-products/', ProductListView.as_view(), name='list_product'),
    path('categories/', CategoryListView.as_view(), name='list_category'),
    path('create-category/', CategoryCreateView.as_view(), name='create_category'),
    path('edit-category/<slug:slug>/', CategoryUpdateView.as_view(), name='update_category'),
    path('delete-category/<slug:slug>/', CategoryDeleteView.as_view(), name='delete_category'),
    path('carts/', CartListView.as_view(), name='list_cart'),
    path('carts/<int:cart_id>', CartDetailView.as_view(), name='list_cart_item'),
]