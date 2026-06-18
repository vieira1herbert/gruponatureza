from django.urls import path

from .views import (
    pdv,
    identificar_revendedor,
    preparar_pagamento,
    pagamento,
    confirmar_venda,
    extrato_venda,
    listar_vendas,
    detalhe_venda
)

urlpatterns = [
    path('pdv/', pdv, name='pdv'),

    path(
        'pdv/preparar-pagamento/',
        preparar_pagamento,
        name='preparar_pagamento'
    ),

    path(
        'pdv/pagamento/',
        pagamento,
        name='pagamento'
    ),

    path(
        'pdv/confirmar/',
        confirmar_venda,
        name='confirmar_venda'
    ),

    path(
        'vendas/extrato/<int:venda_id>/',
        extrato_venda,
        name='extrato_venda'
    ),

    path(
        'vendas/',
        listar_vendas,
        name='listar_vendas'
    ),

    path(
        'vendas/<int:venda_id>/',
        detalhe_venda,
        name='detalhe_venda'
    ),
    path(
    'pdv/revendedor/',
    identificar_revendedor,
    name='identificar_revendedor'
),
]