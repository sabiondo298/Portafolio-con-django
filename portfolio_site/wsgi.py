# apunta wsgi al proyecto para iniciar la aplicación en producción o desarrollo.
import os

from django.core.wsgi import get_wsgi_application

# configura el módulo de settings que usará wsgi.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_site.settings")
application = get_wsgi_application()
