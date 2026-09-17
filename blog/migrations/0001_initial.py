from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160, verbose_name="titulo")),
                ("slug", models.SlugField(blank=True, max_length=180, unique=True, verbose_name="slug")),
                ("excerpt", models.TextField(max_length=280, verbose_name="bajada")),
                ("body", models.TextField(verbose_name="contenido")),
                ("multimedia", models.FileField(blank=True, upload_to="blog/", verbose_name="archivo multimedia")),
                ("published_at", models.DateTimeField(auto_now_add=True, verbose_name="fecha de publicacion")),
            ],
            options={"ordering": ["-published_at"], "verbose_name": "entrada", "verbose_name_plural": "entradas"},
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("author", models.CharField(max_length=80, verbose_name="nombre")),
                ("body", models.TextField(max_length=1000, verbose_name="comentario")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="fecha")),
                ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="blog.post")),
            ],
            options={"ordering": ["created_at"], "verbose_name": "comentario", "verbose_name_plural": "comentarios"},
        ),
    ]
