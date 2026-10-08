# define las rutas públicas del blog y sus acciones de administración.
from django.urls import path

from . import views

app_name = "blog"

# mapea la lista de publicaciones, la creación y la eliminación de entradas y comentarios.
urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("nueva/", views.post_create, name="post_create"),
    path("<slug:slug>/eliminar/", views.post_delete, name="post_delete"),
    path("<slug:slug>/comentarios/<int:comment_id>/eliminar/", views.comment_delete, name="comment_delete"),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
]
