from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import RegexValidator


from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    phone_number_validator = RegexValidator('^09\d{9}$', message="Invalid phone number.")
    # username = None
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        null=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        'email address',
        unique=True
    )
    is_seller = models.BooleanField(default=False)
    phone_number = models.CharField(
        max_length=11,
        null=True,
        unique=True,
        validators=[phone_number_validator]
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    # objects = CustomUserManager()

    def __str__(self):
        return self.username
