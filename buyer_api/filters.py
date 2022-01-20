from django_filters.rest_framework import FilterSet, NumberFilter
from shop.models import *

class ShopFilter(FilterSet):
    class Meta:
        model = Shop
        fields = ['type']


class ProductFilter(FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr='gte')
    max_price = NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'category']

