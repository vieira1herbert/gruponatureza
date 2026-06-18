from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_barras = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome