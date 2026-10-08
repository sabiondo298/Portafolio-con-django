#!/usr/bin/env python
# inicia django y ejecuta la línea de comandos del proyecto.
import os
import sys


# lanza la aplicación con la configuración del proyecto principal.
def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_site.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django no esta instalado. Ejecuta: pip install -r requirements.txt") from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
