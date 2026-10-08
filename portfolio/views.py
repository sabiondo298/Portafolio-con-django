# renderiza la página principal del portfolio.
from django.shortcuts import render


# devuelve la vista inicial que se muestra al entrar al sitio.
def home(request):
    return render(request, "portfolio/home.html")
