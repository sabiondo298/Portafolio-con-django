# importa la interfaz de administración de django y los modelos del blog.
from django.contrib import admin

# importa los modelos que se van a gestionar en el panel de administración.
from .models import Comment, Post, PostMedia


# permite subir y describir archivos multimedia dentro del formulario de creación de una entrada.
class PostMediaInline(admin.TabularInline):
    model = PostMedia
    extra = 1
    min_num = 1
    validate_min = True
    fields = ("file", "caption")


# registra cada entrada con su multimedia y una búsqueda rápida por datos relevantes.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = (PostMediaInline,)
    list_display = ("title", "author", "published_at")
    list_filter = ("published_at",)
    search_fields = ("title", "author", "body")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-published_at",)

    # solo permite borrar posts a usuarios activos, del staff y con permiso explícito.
    def has_delete_permission(self, request, obj=None):
        return (
            request.user.is_active
            and request.user.is_staff
            and request.user.has_perm("blog.delete_post")
        )


# muestra los comentarios en el panel admin y bloquea su eliminación para usuarios sin permiso.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("author", "body")
    readonly_fields = ("post", "author", "body", "created_at")

    # solo permite borrar comentarios a usuarios activos, del staff y con permiso explícito.
    def has_delete_permission(self, request, obj=None):
        return (
            request.user.is_active
            and request.user.is_staff
            and request.user.has_perm("blog.delete_comment")
        )
