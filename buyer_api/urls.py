from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from buyer_api.views import *
from user.views import ApiRegisterView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('v1/cart', CartView, basename='cart')


urlpatterns = [
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/register/', ApiRegisterView.as_view(), name='api_register'),
    path('v1/shop/', ShopListApi.as_view(), name='shop_list_api'),
    path('v1/shop/type/', ShopTypeListApi.as_view(), name='shop_type_list_api'),
    path('v1/shop/<slug:shop_slug>/category/', ShopCategoryListApi.as_view(), name='shop_category_list_api'),
    path('v1/shop/<slug:shop_slug>/product/', ShopProductListApi.as_view(), name='shop_product_List_api'),
    path('v1/product/<slug:slug>/', ShopProductDetailApi.as_view(), name='shop_product_detail_api'),
    # path('v1/cart/', CarView.as_view(), name='cart_view'),
    # path('v1/cart/', include(router.urls)),
]

urlpatterns += router.urls