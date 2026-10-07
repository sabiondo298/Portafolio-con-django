from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_postmedia"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="author",
            field=models.CharField(
                default="Juan Giuri",
                max_length=80,
                verbose_name="nombre del autor",
            ),
        ),
    ]
