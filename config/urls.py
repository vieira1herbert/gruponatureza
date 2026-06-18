from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('dashboard.urls')),
    path('', include('usuarios.urls')),
    path('', include('vendas.urls')),
    path('', include('produtos.urls')),
    path('', include('estoque.urls')),
    path('', include('revendedores.urls')),
        path('', include('franquias.urls')),
]