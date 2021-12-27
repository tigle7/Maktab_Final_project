from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class UserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)