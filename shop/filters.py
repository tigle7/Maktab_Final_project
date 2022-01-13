from django.db.models import fields
import django_filters
from blog.models import Post
from django_filters import DateRangeFilter,DateFilter
from django_filters.widgets import RangeWidget


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
