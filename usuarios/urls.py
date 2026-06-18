from django.urls import path

from .views import (
    UsuarioLoginView,
    sair,
    listar_usuarios,
    cadastrar_usuario,
    editar_usuario
)

urlpatterns = [
    path('login/', UsuarioLoginView.as_view(), name='login'),
    path('logout/', sair, name='logout'),

    path('usuarios/', listar_usuarios, name='listar_usuarios'),

    path(
        'usuarios/cadastrar/',
        cadastrar_usuario,
        name='cadastrar_usuario'
    ),
    path(
    'usuarios/editar/<int:usuario_id>/',
    editar_usuario,
    name='editar_usuario'
),
]