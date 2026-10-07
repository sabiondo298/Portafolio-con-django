# Portfolio y blog personal

Sitio personal hecho con Django. El portfolio y el blog comparten navegación, tipografía, paleta de colores y cambio de tema.

## Organización

```text
portfolio_site/       Configuración y rutas del proyecto Django
portfolio/            Aplicación de la portada del portfolio
blog/                 Entradas, archivos multimedia, comentarios y administración
templates/base.html   Plantilla compartida
static/css/           Estilos del sitio
static/js/            Interacciones del sitio y del portfolio
static/images/        Imágenes y CV
media/blog/           Archivos multimedia que se cargan desde el admin
```

## Funcionalidad del blog

- Las entradas se publican desde `/admin/` y se muestran de la más nueva a la más antigua.
- Cada entrada incluye título, bajada, texto y al menos un archivo multimedia.
- El admin admite imágenes, videos, audios y PDF de hasta 20 MB por archivo.
- Las personas pueden comentar sin crear una cuenta; el administrador puede revisar y eliminar los comentarios desde el admin.
- El listado muestra seis entradas por página.

## Puesta en marcha

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Portfolio: `http://127.0.0.1:8000/`
- Blog: `http://127.0.0.1:8000/blog/`
- Administración: `http://127.0.0.1:8000/admin/`

Los archivos cargados se guardan en `media/`; en desarrollo Django también los sirve desde esa carpeta.
