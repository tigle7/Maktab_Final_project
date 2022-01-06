from django.urls import path, re_path
from shop.views.shop_view import *

# app_name = 'shop'

urlpatterns = [
    path('dashboard/', ShopListView.as_view(), name='shop_dashboard'),
    path('dashboard/create-shop/', ShopCreateView.as_view(), name='create_shop'),
    path('dashboard/edit-shop/<slug:slug>/', ShopEditView.as_view(), name='edit_shop'),
    path('dashboard/delete-shop/<slug:slug>/', ShopDeleteView.as_view(), name='delete_shop'),
    path('dashboard/<slug:slug>', ShopDetailView.as_view(), name='shop_detail'),


]