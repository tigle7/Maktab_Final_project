from django.db.models import fields
import django_filters
from shop.models import *

class ShopFilter(django_filters.FilterSet):
    class Meta:
        model = Shop
        fields = ['type']