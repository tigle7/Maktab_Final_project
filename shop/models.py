from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class GeneralModel(models.Model):

    created_at = models.DateTimeField(
        verbose_name=_('Created Time'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated Time'),
        auto_now=True
    )

    class Meta:
        abstract = True


class Category(GeneralModel):

    title = models.CharField(
        verbose_name=_("Category Title"),
        max_length=250
    )
    slug = models.SlugField(
        max_length=255,
        unique=True
    )
    author = models.ForeignKey(
        User,
        verbose_name=_('Category Author'),
        related_name='product_category_author',
        null=True,
        on_delete=models.SET_NULL,
    )

    def get_absolute_url(self):
        return reverse('category_list')

    def __str__(self):
        return self.title


class Product(GeneralModel):

    category = models.ForeignKey(
        Category,
        related_name='product_category',
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='product_creator'
    )
    title = models.CharField(
        max_length=255
    )
    author = models.CharField(
        max_length=255,
        default='admin'
    )
    description = models.TextField(
        blank=True
    )
    image = models.ImageField(
        upload_to='uploads',
        default='uploads/default.jpg'
    )
    slug = models.SlugField(
        max_length=255
    )
    is_available = models.BooleanField(
        default=True
    )
    price = models.PositiveBigIntegerField()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created_at',)

    # def get_absolute_url(self):
    #     return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title


class Shop(GeneralModel):

    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('C', 'Confirmed'),
        ('D', 'Deleted')
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='P'
    )
    title = models.CharField(
        max_length=255
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    proucts = models.ManyToManyField(
        Product,
        related_name='proucts'
    )

    def __str__(self):
        return f'{self.title} Shop'


class CartItem(GeneralModel):

    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return f"{self.quantity} of {self.product}"


class Cart(GeneralModel):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="carts"
    )
    items = models.ManyToManyField(
        CartItem,
        related_name='items'
    )
    ordered = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.owner.username
