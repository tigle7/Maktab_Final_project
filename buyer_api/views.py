from django.shortcuts import render
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView, ListAPIView, RetrieveAPIView)
# from rest_framework.mixins import *
from rest_framework.permissions import IsAuthenticated
from shop.models import *
from .serializers import *
from .filters import *
from django.shortcuts import get_object_or_404
# Create your views here.

User = get_user_model()


class ShopListApi(ListAPIView):

    queryset = Shop.confirmed.all()
    serializer_class = ShopSerializer
    filterset_class = ShopFilter


class ShopTypeListApi(ListAPIView):

    queryset = ShopType.objects.all()
    serializer_class = ShopTypeSerializer


class ShopCategoryApi(ListAPIView):

    serializer_class = ShopCategorySerializer

    def get_queryset(self):
        shop = get_object_or_404(Shop, slug=self.kwargs['shop_slug'])
        queryset = Category.objects.filter(author=shop.owner)
        return queryset


class ShopProductApi(ListAPIView):

    serializer_class = ProductSerializer

    def get_queryset(self):
        shop = get_object_or_404(Shop, slug=self.kwargs['shop_slug'])
        queryset = Product.available.filter(shop=shop)
        return queryset
