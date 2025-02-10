from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug','publish','status']
    list_filter = ['status', 'created', 'publish','author']
    prepopulated_fields={'slug':('title',)}

@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['post', 'name', 'created', 'active']
    list_filter = ['active', 'created']
    search_fields = ['name', 'email', 'body']

