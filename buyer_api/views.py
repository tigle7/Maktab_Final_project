from django.shortcuts import render
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView,
    ListCreateAPIView, ListAPIView, RetrieveAPIView, CreateAPIView)
# from rest_framework.mixins import *
from rest_framework.permissions import IsAuthenticated
from shop.models import *
from .serializers import *
from .filters import *
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import parsers, renderers
# Create your views here.

User = get_user_model()


class ShopListApi(ListAPIView):
    
    # permission_classes = [IsAuthenticated]
    queryset = Shop.confirmed.all()
    serializer_class = ShopSerializer
    filterset_class = ShopFilter


class ShopTypeListApi(ListAPIView):

    queryset = ShopType.objects.all()
    serializer_class = ShopTypeSerializer


class ShopCategoryListApi(ListAPIView):

    serializer_class = ShopCategorySerializer

    def get_queryset(self):
        shop = get_object_or_404(Shop, slug=self.kwargs['shop_slug'])
        queryset = Category.objects.filter(author=shop.owner)
        return queryset


class ShopProductListApi(ListAPIView):

    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    def get_queryset(self):
        shop = get_object_or_404(Shop, slug=self.kwargs['shop_slug'])
        queryset = Product.objects.filter(shop=shop)
        return queryset

class ShopProductDetailApi(RetrieveUpdateAPIView):

    # parser_classes = (parsers.MultiPartParser)
    model = Product
    queryset = Product.objects.all()
    http_method_names = ['put', 'get']
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    # throttle_classes = ()
    # permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)

    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs['slug'])

class CartView(ModelViewSet):
    # serializer_class = AddItemToCartSerializer
    # model = CartItem
    def list(self, request):
        obj, _ = Cart.objects.get_or_create(owner=request.user, status="N")
        # Remove unavailable items from cart
        unavailable_items = obj.items.filter(product__active=False)
        if unavailable_items.exists():
            unavailable_items.delete()
        serializer = CartSerializer(obj, context={'request': request})
        return Response(serializer.data)

    def get_queryset(self):
        return self.request.user.carts.get(status='N').items.all()

    def get_serializer_class(self):
        if self.action == "create":
            return AddItemToCartSerializer
        return CartItemSerializer


# class CreateCustomerProfileView(CreateAPIView):
#     parser_classes = (MultiPartParser, FormParser)
#     model = Customer
#     permission_classes = [
#         permissions.IsAuthenticated  # Or anon users can't register
#     ]
#     serializer_class = ProfileSerializer


# class CustomerProfileUpdateDetailٰView(RetrieveUpdateAPIView):
#     http_method_names = ['put', 'get']
#     parser_classes = (MultiPartParser, FormParser)
#     model = Customer
#     queryset = Customer.objects.all()
#     serializer_class = ProfileSerializer
#     permission_classes = [
#         permissions.IsAuthenticated  # Or anon users can't register
#     ]

#     def get_object(self):
#         return get_object_or_404(Customer, custom_user_id=self.request.user.id)