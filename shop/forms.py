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
        fields = ['title', 'category', 'description', 'image', 'price']