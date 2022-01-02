from django.urls import path, re_path
from .views import *

# app_name = 'shop'

urlpatterns = [
    path('dashboard/', ShopListView.as_view(), name='shop_dashboard'),
]