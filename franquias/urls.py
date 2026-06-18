from django.urls import path

from .views import (
    listar_franquias,
    cadastrar_franquia,
    editar_franquia
)

urlpatterns = [
    path('franquias/', listar_franquias, name='listar_franquias'),
    path('franquias/cadastrar/', cadastrar_franquia, name='cadastrar_franquia'),
    path('franquias/editar/<int:franquia_id>/', editar_franquia, name='editar_franquia'),
    
]