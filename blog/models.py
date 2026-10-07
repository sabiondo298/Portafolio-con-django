from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from .validators import validate_media_size


class Post(models.Model):
    title = models.CharField("titulo", max_length=160)
    author = models.CharField("nombre del autor", max_length=80, default="Juan Giuri")
    slug = models.SlugField("slug", max_length=180, unique=True, blank=True)
    excerpt = models.TextField("bajada", max_length=280)
    body = models.TextField("contenido")
    published_at = models.DateTimeField("fecha de publicacion", auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "entrada"
        verbose_name_plural = "entradas"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            suffix = 2
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{suffix}"
                suffix += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(
        "archivo",
        upload_to="blog/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "jpg",
                    "jpeg",
                    "png",
                    "gif",
                    "webp",
                    "mp4",
                    "webm",
                    "ogv",
                    "mp3",
                    "wav",
                    "ogg",
                    "pdf",
                ]
            ),
            validate_media_size,
        ],
    )
    caption = models.CharField("descripcion", max_length=180, blank=True)

    class Meta:
        verbose_name = "archivo multimedia"
        verbose_name_plural = "archivos multimedia"

    @property
    def media_type(self):
        extension = self.file.name.rsplit(".", 1)[-1].lower()
        if extension in {"jpg", "jpeg", "png", "gif", "webp"}:
            return "image"
        if extension in {"mp4", "webm", "ogv"}:
            return "video"
        if extension in {"mp3", "wav", "ogg"}:
            return "audio"
        return "file"

    def __str__(self):
        return self.caption or self.file.name.rsplit("/", 1)[-1]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.CharField("nombre", max_length=80)
    body = models.TextField("comentario", max_length=1000)
    created_at = models.DateTimeField("fecha", auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "comentario"
        verbose_name_plural = "comentarios"

    def __str__(self):
        return f"{self.author} en {self.post}"
