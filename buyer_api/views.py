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
from django.db.models import Q
# Create your views here.

User = get_user_model()


class ShopListView(ListAPIView):
    
    # permission_classes = [IsAuthenticated]
    queryset = Shop.confirmed.all()
    serializer_class = ShopSerializer
    filterset_class = ShopFilter


class ShopTypeListView(ListAPIView):

    queryset = ShopType.objects.all()
    serializer_class = ShopTypeSerializer


class ShopCategoryListView(ListAPIView):

    serializer_class = ShopCategorySerializer

    def get_queryset(self):
        shop = get_object_or_404(Shop, slug=self.kwargs['shop_slug'])
        queryset = Category.objects.filter(author=shop.owner)
        return queryset


class ShopProductListView(ListAPIView):

    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    def get_queryset(self):
        shop = get_object_or_404(Shop, slug=self.kwargs['shop_slug'])
        queryset = Product.objects.filter(shop=shop)
        return queryset

class ShopProductDetailView(RetrieveUpdateAPIView):

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

    parser_classes = (parsers.FormParser,)
    
    def list(self, request):
        obj, _ = Cart.objects.get_or_create(owner=request.user, status="N")
        # Remove unavailable items from cart
        # unavailable_items = obj.items.filter(Q(product__active=False) | Q(product__quantity__lte=0))
        items = obj.items.all()
        for unavailable_item in items:
            if not (unavailable_item.product.is_available and unavailable_item.is_available_quantity):
                unavailable_item.delete()
        serializer = CartSerializer(obj, context={'request': request})
        return Response(serializer.data)

    def get_queryset(self):
        return self.request.user.carts.get(status='N').items.all()

    def get_serializer_class(self):
        if self.action == "create":
            return AddItemToCartSerializer
        return CartItemSerializer

class OrderView(ListCreateAPIView):

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.orders.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        return OrderListSerializer

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