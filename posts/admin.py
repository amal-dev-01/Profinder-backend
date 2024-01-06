from django.contrib import admin

from .models import Comment, Like, Post

# Register your models here.


@admin.register(Post)
class Post(admin.ModelAdmin):
    list_display = ("title", "user")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
