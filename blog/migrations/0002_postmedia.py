import django.core.validators
from django.db import migrations, models
import django.db.models.deletion

import blog.validators


def move_legacy_media(apps, _schema_editor):
    Post = apps.get_model("blog", "Post")
    PostMedia = apps.get_model("blog", "PostMedia")
    database = _schema_editor.connection.alias

    for post in Post.objects.using(database).exclude(multimedia="").iterator():
        PostMedia.objects.using(database).create(post_id=post.pk, file=post.multimedia.name)


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PostMedia",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to="blog/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
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
                            blog.validators.validate_media_size,
                        ],
                        verbose_name="archivo",
                    ),
                ),
                (
                    "caption",
                    models.CharField(blank=True, max_length=180, verbose_name="descripcion"),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="media",
                        to="blog.post",
                    ),
                ),
            ],
            options={
                "verbose_name": "archivo multimedia",
                "verbose_name_plural": "archivos multimedia",
            },
        ),
        migrations.RunPython(move_legacy_media, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="post",
            name="multimedia",
        ),
    ]
