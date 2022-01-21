from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from buyer_api.views import *
from user.views import ApiRegisterView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('cart', CartView, basename='cart')


urlpatterns = [
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', ApiRegisterView.as_view(), name='api_register'),
    path('profile/', CustomerProfilelView.as_view(), name='api_profile_view'),
    path('shop/', ShopListView.as_view(), name='shop_list_api'),
    path('shop/type/', ShopTypeListView.as_view(), name='shop_type_list_api'),
    path('shop/<slug:shop_slug>/category/', ShopCategoryListView.as_view(), name='shop_category_list_api'),
    path('shop/<slug:shop_slug>/product/', ShopProductListView.as_view(), name='shop_product_List_api'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='shop_product_detail_api'),
    path('order/', OrderView.as_view(), name='payment_view'),
]

urlpatterns += router.urls