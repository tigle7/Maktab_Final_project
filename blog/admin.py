from django.contrib import admin
from .models import Post, Comment, Category

# class PostAdmin(admin.ModelAdmin):
#     exclude = ('slug',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'create_at', 'slug')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Category)


