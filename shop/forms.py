import imp
from django import forms
from .models import *
from user.models import CustomUser

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['title', 'type', 'image', ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'quantity', 'price',
         'discount_price', 'active', 'image', 'description']
                  

        # exclude = ('updated_at', 'owner', 'shop',  )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('owner')
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(author=user)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'parent']

class ProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields=["username" , "email" , "phone_number" , "image" , "address" ,"city"]

