from django import forms
from .models import *


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['title', 'type', 'image', ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'price', 'discount_price',
                  'description', 'is_available', 'image']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('owner')
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(author=user)


class CategoryForm(forms.ModelForm):
    class meta:
        model = Category
        fields = ['title', 'parent']

class TestForm(forms.Form):
    title = forms.CharField(required=False)