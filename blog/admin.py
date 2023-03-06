from django.contrib import admin
from .models import Category, Post, PostComment

admin.site.register(Category)
admin.site.register(PostComment)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created', 'active', 'featured']
