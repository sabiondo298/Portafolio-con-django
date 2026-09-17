from django.contrib import admin

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at")
    list_filter = ("published_at",)
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-published_at",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("author", "body")
    readonly_fields = ("created_at",)
