from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField("titulo", max_length=160)
    slug = models.SlugField("slug", max_length=180, unique=True, blank=True)
    excerpt = models.TextField("bajada", max_length=280)
    body = models.TextField("contenido")
    multimedia = models.FileField("archivo multimedia", upload_to="blog/", blank=True)
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
