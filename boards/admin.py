from django.contrib import admin

from .models import Comment, Post, Reply


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "content", "writer", "category", "like_count", "view_count", "updated_at")
    list_filter = ("writer", "updated_at", "category")
    search_fields = ("id", "title")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "content", "writer", "updated_at")
    list_filter = ("writer", "updated_at")
    search_fields = ("post__id", "id", "content")


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("id", "comment", "content", "writer", "updated_at")
    list_filter = ("writer", "updated_at")
    search_fields = ("comment__id", "id", "content")
