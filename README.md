# Portfolio y blog de Juan Giuri

Sitio personal desarrollado con Django. La portada conserva la composición original del portfolio y el blog permite publicar entradas con texto, adjuntar archivos multimedia y recibir comentarios.

## Puesta en marcha

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/` para el portfolio, `http://127.0.0.1:8000/blog/` para el blog y `/admin/` para administrar entradas y eliminar comentarios.

Las entradas solo se crean desde el admin. Los visitantes pueden comentar sin registrarse; el administrador puede moderar y eliminar esos comentarios.