from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('id', 'owner', 'total_price',
                    'items_count', 'status', 'created_at')
    list_display_links = ('id', 'owner')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    list_per_page = 25
    search_fields = ('owner__phone_number', 'owner__email',
                     'items__product__title')
    actions = ['make_canceled']

    @admin.action(description='Make selected Cart as canceled')
    def make_canceled(self, request, queryset):
        rows = queryset.update(status='C')
        self.message_user(request, f'{rows} updated')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'total_price', 'price')
    list_display_links = ('id', 'cart')
    list_per_page = 25
    search_fields = ('cart__owner__phone_number',
                     'cart__owner__email', 'product__title')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('show_image', 'id', 'title', 'quantity','price',
                    'is_available', 'active', 'owner', 'shop')
    list_filter = ('created_at', 'owner', 'shop')
    search_fields = ('title',)
    list_per_page = 25
    list_editable = ('price', 'quantity', 'active')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('is_available',)
    # raw_id_fields = ('category',)
    # actions = ('make_available',)

    @admin.display(empty_value='-', description="show image")
    def show_image(self, obj):
        if (obj.image):
            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.image.url,
            )
        return '-'

    # @admin.action(description='Make selected products available')
    # def make_available(self, request, queryset):
    #     rows = queryset.update(is_available=True)
    #     self.message_user(request, f'{rows} updated')


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):

    list_display = ('title', 'status', 'owner')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    actions = ['make_confirmed']
    search_fields = ('title', 'owner')
    prepopulated_fields = {'slug': ('title',)}

    @admin.action(description='Make selected Shops as confirmed')
    def make_confirmed(self, request, queryset):
        rows = queryset.update(status='C')
        self.message_user(request, f'{rows} updated')


@admin.register(ShopType)
class ShopTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('owner', 'cart', 'created_at')

# admin.site.register(Order)