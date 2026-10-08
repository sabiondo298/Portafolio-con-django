# define las rutas de la portada del sitio.
from django.urls import path

from . import views

app_name = "portfolio"

# configura la ruta principal del portfolio.
urlpatterns = [
    path("", views.home, name="home"),
]
