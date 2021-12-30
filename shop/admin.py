from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.

# admin.site.register(Cart)
admin.site.register(CartItem)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('title', 'price', 'is_available', 'show_image')
    list_filter = ('is_available', 'created_at')
    list_editable = ('price',)
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('category',)
    actions = ('make_available',)

    @admin.display(empty_value='-', description="show image")
    def show_image(self, obj):
        if (obj.image):
            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.image.url,
            )
        return '-'

    @admin.action(description='Make selected products available')
    def make_available(self, request, queryset):
        rows = queryset.update(is_available=True)
        self.message_user(request, f'{rows} updated')


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):

    list_display = ('title', 'status', 'owner')
    list_filter = ('status', 'created_at')
    actions = ['make_confirmed']

    @admin.action(description='Make selected Shops as confirmed')
    def make_confirmed(self, request, queryset):
        rows = queryset.update(status='C')
        self.message_user(request, f'{rows} updated')

@admin.register(ShopType)
class ShopTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    
    list_display = ('owner', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    actions = ['make_canceled']


    @admin.action(description='Make selected Cart as canceled')
    def make_canceled(self, request, queryset):
        rows = queryset.update(status='C')
        self.message_user(request, f'{rows} updated')
