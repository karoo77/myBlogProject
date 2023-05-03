from django.contrib import admin
from .models import Author, Post


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bio', 'avatar', 'is_active']
    list_filter = ['is_active', 'create_time', 'update_time']
    search_fields = ['user__username', 'bio']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'is_active']
    list_filter = ['is_active', 'create_time', 'update_time']
    search_fields = ['title', 'author__user__username']