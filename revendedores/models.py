from django.db import models
from franquias.models import Franquia


class Revendedor(models.Model):
    franquia = models.ForeignKey(
        Franquia,
        on_delete=models.PROTECT,
        related_name='revendedores',
        null=True,
        blank=True
    )

    nome = models.CharField(max_length=120)
    cpf = models.CharField(max_length=14, unique=True)

    codigo = models.PositiveIntegerField(
        unique=True,
        null=True,
        blank=True
    )

    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def save(self, *args, **kwargs):

        if not self.codigo:
            ultimo = Revendedor.objects.order_by('-codigo').first()

            if ultimo and ultimo.codigo:
                self.codigo = ultimo.codigo + 1
            else:
                self.codigo = 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nome} - {self.codigo}'