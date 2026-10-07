from django.contrib import admin

from .models import Comment, Post, PostMedia


class PostMediaInline(admin.TabularInline):
    model = PostMedia
    extra = 1
    min_num = 1
    validate_min = True
    fields = ("file", "caption")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = (PostMediaInline,)
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
    readonly_fields = ("post", "author", "body", "created_at")
