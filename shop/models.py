from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .managers import ConfirmedShopManager, AvailableProductManager
from django.utils.text import slugify
from random import randint
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class ShopType(GeneralModel):

    title = models.CharField(
        verbose_name=_("Shop Type Title"),
        max_length=250
    )
    slug = models.SlugField(
        max_length=255,
        unique=True
    )
    author = models.ForeignKey(
        User,
        verbose_name=_('Shop Type Author'),
        related_name='shop_type_author',
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.title


class Category(GeneralModel):

    title = models.CharField(
        verbose_name=_("Category Title"),
        max_length=250
    )
    slug = models.SlugField(
        max_length=255,
        unique=True
    )
    parent = models.ForeignKey(
        "self",
        verbose_name="Category Parent",
        related_name='category_parent',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        User,
        verbose_name=_('Category Author'),
        related_name='product_category_author',
        null=True,
        on_delete=models.SET_NULL,
    )

    def get_absolute_url(self):
        return reverse('list_category')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            if Category.objects.filter(title=self.title).exists() or Category.objects.filter(slug=self.title).exists():
                add_rand = str(randint(1, 10000))
                self.slug = slugify(self.title) + "-" + add_rand
            else:
                self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class Product(GeneralModel):

    category = models.ForeignKey(
        Category,
        related_name='product_category',
        null=True,
        on_delete=models.SET_NULL
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='product_creator'
    )
    title = models.CharField(
        max_length=255
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='uploads',
        default='uploads/default.jpg'
    )
    slug = models.SlugField(
        max_length=255,
        blank=True
    )
    # is_available = models.BooleanField(
    #     default=True
    # )
    quantity = models.PositiveIntegerField(
        default=1
    )
    shop = models.ForeignKey(
        'Shop',
        on_delete=models.CASCADE,
        null=True,
        related_name='product_shop'
    )
    active = models.BooleanField(default=True)
    price = models.PositiveBigIntegerField()
    description = models.TextField()
    

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created_at',)

    objects = models.Manager()
    available = AvailableProductManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            if Product.objects.filter(title=self.title).exists() or Product.objects.filter(slug=self.title).exists():
                add_rand = str(randint(1, 10000))
                self.slug = slugify(self.title) + "-" + add_rand
            else:
                self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop_detail', kwargs={'slug': self.shop.slug})

    def __str__(self):
        return self.title

    @property
    def is_available(self):
        return self.quantity > 0 and self.active

    @property
    def discount_percent(self):
        if self.discount_price:
            discount_percent = 100 - (self.discount_price * 100) / self.price
            return int(discount_percent)
        return

    @property
    def final_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price


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
    type = models.ForeignKey(
        ShopType,
        related_name='shop_type',
        null=True,
        on_delete=models.SET_NULL
    )
    image = models.ImageField(
        upload_to='uploads',
        default='uploads/default.jpg'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )
    objects = models.Manager()
    confirmed = ConfirmedShopManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            if Shop.objects.filter(title=self.title).exists() or Shop.objects.filter(slug=self.title).exists():
                add_rand = str(randint(1, 10000))
                self.slug = slugify(self.title) + "-" + add_rand
            else:
                self.slug = slugify(self.title)
        super(Shop, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.title} Shop'


class CartItem(GeneralModel):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        default=1
    )
    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
        related_name='items',
        null=True
    )
    price = models.PositiveBigIntegerField(
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f"{self.quantity} of {self.product}"

    @property
    def shop(self):
        return self.product.shop
    
    @property
    def available_quantity(self):
        return self.quantity <= self.product.quantity

    @property
    def total_price(self):
        if self.cart.status == 'N':
            return self.product.final_price * self.quantity
        return self.price * self.quantity


class Cart(GeneralModel):

    STATUS_CHOICES = (
        ('P', 'Paid'),
        ('N', 'Not paid'),
        ('C', 'Canceled')
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='N'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="carts"
    )
    shop = models.ForeignKey(
        "Shop",
        on_delete=models.SET_NULL,
        null=True
    )

    #  @property
    # def shop(self):
    #     return self.items.first().shop

    # items = models.ManyToManyField(
    #     CartItem,
    #     related_name='items'
    # )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.owner.username} Cart ({self.created_at})'

    @property
    def total_price(self):
        total_price = 0
        for item in self.items.all():
            total_price += item.total_price
        return total_price

    @property
    def total_count(self):
        total_count = 0
        for item in self.items.all():
            total_count += item.quantity
        return total_count

    @property
    def items_count(self):
        return self.items.all().count()

    class Meta:
        ordering = ('-created_at',)

@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    """ When user registered create cart model with this user """
    if created:
        Cart.objects.create(owner=instance)

