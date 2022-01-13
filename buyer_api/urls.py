from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from buyer_api.views import *
from user.views import ApiRegisterView


urlpatterns = [
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/register/', ApiRegisterView.as_view(), name='api_register'),
    path('v1/shop/', ShopListApi.as_view(), name='shop_list_api'),
    path('v1/shop/type/', ShopTypeListApi.as_view(), name='shop_type_list_api'),
    path('v1/shop/<slug:shop_slug>/category/', ShopCategoryApi.as_view(), name='shop_category_list_api'),
    path('v1/shop/<slug:shop_slug>/product/', ShopProductApi.as_view(), name='shop_product_list_api'),


    
]