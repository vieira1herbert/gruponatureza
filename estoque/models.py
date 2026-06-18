from django.db import models
from produtos.models import Produto
from franquias.models import Franquia


class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    franquia = models.ForeignKey(Franquia, on_delete=models.CASCADE)

    quantidade = models.PositiveIntegerField(default=0)
    estoque_minimo = models.PositiveIntegerField(default=5)

    class Meta:
        unique_together = ('produto', 'franquia')

    def __str__(self):
        return f'{self.produto.nome} - {self.franquia.nome}'

    def estoque_baixo(self):
        return self.quantidade <= self.estoque_minimo