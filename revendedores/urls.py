from django.urls import path

from .views import (
    listar_revendedores,
    cadastrar_revendedor,
    editar_revendedor
)

urlpatterns = [
    path('revendedores/', listar_revendedores, name='listar_revendedores'),
    path('revendedores/cadastrar/', cadastrar_revendedor, name='cadastrar_revendedor'),
    path('revendedores/editar/<int:revendedor_id>/', editar_revendedor, name='editar_revendedor'),
]