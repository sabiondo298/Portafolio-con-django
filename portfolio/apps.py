# configura la app portfolio dentro del proyecto django.
from django.apps import AppConfig


# define la configuración de la app portfolio.
class PortfolioConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "portfolio"
