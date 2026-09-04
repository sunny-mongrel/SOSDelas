from django.contrib import admin
from django.urls import path, include  # Não esqueça de importar o include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('paginas.urls')),  # Isso joga a inicial para o seu app paginas
]
