from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_editable = ('is_seller',)
    list_display = ('email', 'is_seller', 'is_staff', 'is_active','last_name',)
    list_filter = ('is_staff', 'is_active', 'is_seller')
    # fieldsets = (
    #     (None, {'fields': ('email', 'password')}),
    #     ('Permissions', {'fields': ('is_staff', 'is_active', 'is_seller')}),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
    #     ),
    # )
    search_fields = ('email',)
    ordering = ('email',)
    actions = ['make_seller']
    
    @admin.action(description='Make selected User as seller')
    def make_seller(self, request, queryset):
        rows = queryset.update(is_seller=1)
        self.message_user(request, f'{rows} updated')
