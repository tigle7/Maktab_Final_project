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
    def __init__(self, *args, **kwargs):
       user = kwargs.pop('user')
       super(PostForm, self).__init__(*args, **kwargs)
       self.fields['category'].queryset = Category.objects.filter(author=user)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']