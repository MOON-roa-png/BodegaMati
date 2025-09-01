from django.contrib import admin
from django.urls import path
from django.http import HttpResponse  # Importamos HttpResponse

# Vista simple de Hola Mundo
def hola_mundo(request):
    return HttpResponse("¡Hola Mundo desde Django! 🚀")

# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),  # Panel de administración
    path('', hola_mundo),             # Ruta principal para Hola Mundo
]
