from itertools import product
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.db.models import F
from rest_framework import serializers
from shop.models import *

User = get_user_model()


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ["id", "title", "type", "slug", "image"]


class ShopTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopType
        fields = ["id", "title", "slug"]


class ShopCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "slug", "parent"]


class ProductSerializer(serializers.ModelSerializer):

    is_available = serializers.SerializerMethodField()
    image = serializers.ImageField()

    class Meta:
        model = Product
        exclude = ('active', 'updated_at', 'owner', )
        extra_kwargs = {
            'slug': {'read_only': True},
        }
    def get_is_available(self, obj):
        return obj.is_available

class ProductDetailSerializer(serializers.ModelSerializer):

    image = serializers.ImageField()

    is_in_cart = serializers.SerializerMethodField()
    discount_percent = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_discount_percent(self, obj):
        return obj.discount_percent

    def get_is_in_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.carts.get(status="N").items.filter(product=obj.id).exists()
        return False


class CartItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ('cart',)

    def get_total_price(self, obj):
        return obj.total_price



class CartSerializer(serializers.ModelSerializer):

    total_price = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'

    def get_total_price(self, obj):
        return obj.total_price

    def get_items_count(self, obj):
        return obj.items_count



class AddItemToCartSerializer(serializers.ModelSerializer):
    cart_items_count = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('product', 'quantity', 'cart_items_count')

    def validate_product(self, product):
        if not product.is_available:
            raise serializers.ValidationError("product is not available.")
        return product

    def create(self, validated_data):
        user = self.context.get('request').user
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        cart, _ = Cart.objects.get_or_create(owner=user, status='N')
        cart_item = CartItem.objects.filter(cart=cart, product=product)
        if cart_item.exists():
            cart_item = cart_item.first()
            if cart_item.quantity <= product.quantity - quantity:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                raise serializers.ValidationError("product quantity is not enough.")
            return cart_item
        else:
            if product.quantity < quantity:
                raise serializers.ValidationError("product quantity is not enough.")
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        return cart_item

    def get_cart_items_count(self, obj):
        user = self.context.get('request').user
        return user.carts.get(status='N').items.count()

class CreateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        exclude = ('updated_at', 'shipping_status')
        read_only_fields = ('cart', 'owner',)

    def create(self, data):
        user = self.context.get('request').user
        cart = user.carts.get(status='N')
        # Validate cart
        items = cart.items.all()
        for unavailable_item in items:
            if not (unavailable_item.product.is_available and unavailable_item.is_available_quantity):
                unavailable_item.delete()
        if not cart.items.all().exists():
            raise serializers.ValidationError("Cart must not be empty")
        # Update products quantity & CartItem price
        for item in cart.items.all():
            Product.objects.filter(id=item.product.id).update(quantity=F('quantity') - item.quantity)
            item.price = item.product.final_price
            item.save()
        cart.status = 'P'
        cart.save()
        order = Order.objects.create(
            owner=user, cart=cart, shipping_status="Preparation")
        # Create another cart model with status not paid
        Cart.objects.create(owner=user)
        return order

class OrderListSerializer(serializers.ModelSerializer):
    
    total_price = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'
        # depth = 1
    def get_total_price(self, obj):
        total_price = 0
        for item in obj.cart.items.all():
            total_price += item.total_price
        return total_price

    def get_items_count(self, obj):
        return obj.cart.items.all().count()

# class ProfileSerializer(serializers.ModelSerializer):

#     image = serializers.ImageField()

#     class Meta:
#         model = User
#         fields = ["customer_username", "country", "state",
#                   "city", "address", "post_code", "custom_user", "image"]
#         related_fields = ["custom_user"]
#         extra_kwargs = {
#             'custom_user': {'read_only': True},
#         }

    # def update(self, instance, validated_data):
    #     # related object available
    #     try:
    #         # Handle related objects
    #         for related_obj_name in self.Meta.related_fields:

    #             # Validated data will show the nested structure
    #             data = validated_data.pop(related_obj_name)
    #             related_instance = getattr(instance, related_obj_name)

    #             # Same as default update implementation
    #             for attr_name, value in data.items():
    #                 setattr(related_instance, attr_name, value)
    #             related_instance.save()
    #     except:
    #         pass
    #     return super(ProfileSerializer, self).update(instance, validated_data)