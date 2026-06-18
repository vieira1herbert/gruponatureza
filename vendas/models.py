import random

from django.db import models
from django.conf import settings

from franquias.models import Franquia
from produtos.models import Produto
from revendedores.models import Revendedor


def gerar_codigo_pedido():
    return str(random.randint(100000000, 999999999))


class Venda(models.Model):

    FORMAS_PAGAMENTO = (
        ('boleto_1x', 'Boleto 1x'),
        ('boleto_2x', 'Boleto 2x'),
        ('boleto_3x', 'Boleto 3x'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('pix', 'Pix'),
        ('dinheiro', 'Dinheiro'),
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    franquia = models.ForeignKey(
        Franquia,
        on_delete=models.PROTECT
    )

    revendedor = models.ForeignKey(
    Revendedor,
    on_delete=models.PROTECT,
    null=True,
    blank=True
)

    codigo_pedido = models.CharField(
        max_length=9,
        unique=True,
        null=True,
        blank=True
    )

    forma_pagamento = models.CharField(
    max_length=30,
    choices=FORMAS_PAGAMENTO,
    null=True,
    blank=True
)

    data = models.DateTimeField(auto_now_add=True)

    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def save(self, *args, **kwargs):

        if not self.codigo_pedido:

            codigo = gerar_codigo_pedido()

            while Venda.objects.filter(
                codigo_pedido=codigo
            ).exists():

                codigo = gerar_codigo_pedido()

            self.codigo_pedido = codigo

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Pedido #{self.codigo_pedido}'


class ItemVenda(models.Model):

    venda = models.ForeignKey(
        Venda,
        related_name='itens',
        on_delete=models.CASCADE
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT
    )

    quantidade = models.PositiveIntegerField()

    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f'{self.produto.nome} x {self.quantidade}'