from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category',]
        file = forms.ImageField
        

        widgets = {
            'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']