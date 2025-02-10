from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug','publish','status']
    list_filter = ['status', 'created', 'publish','author']
    prepopulated_fields={'slug':('title',)}

# Register your models here.
