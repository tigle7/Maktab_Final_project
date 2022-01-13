from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

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
    class Meta:
        model = Product
        fields = ["id", "title", "category", "slug", "image",
                  'discount_price', 'price', 'description']

