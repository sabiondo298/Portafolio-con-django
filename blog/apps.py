# configura la app blog dentro del proyecto django.
from django.apps import AppConfig


# define la configuración de la app blog.
class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"
