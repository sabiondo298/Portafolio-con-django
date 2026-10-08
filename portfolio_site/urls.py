# incluye las rutas del portfolio y del blog, y activa los archivos media en modo debug.
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# define las rutas principales del sitio y la carga de archivos media.
urlpatterns = [
    path("", include("portfolio.urls", namespace="portfolio")),
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
