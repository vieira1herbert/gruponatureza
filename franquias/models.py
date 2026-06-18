from django.db import models


class Franquia(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.nome