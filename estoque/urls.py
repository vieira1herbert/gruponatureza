from django.urls import path
from .views import listar_estoque, editar_estoque

urlpatterns = [
    path('estoque/', listar_estoque, name='listar_estoque'),
    path('estoque/editar/<int:estoque_id>/', editar_estoque, name='editar_estoque'),
]