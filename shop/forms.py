from django import forms
from .models import *


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['title', 'type', 'image',]
        success_message = "Shop successfully created!"
        file = forms.ImageField


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'price', 'description', 'is_available', 'image']

    def __init__(self, *args, **kwargs):
       user = kwargs.pop('owner')
       super(ProductForm, self).__init__(*args, **kwargs)
       self.fields['category'].queryset = Category.objects.filter(author=user)